/**
 * Secure Smart Contract Deployment
 * Protege private key e valida ambiente antes de deploy
 */

const hre = require("hardhat");
const fs = require("fs");
require("dotenv").config();

async function validateEnvironment() {
  console.log("🔍 Validating environment...\n");

  const required = [
    "PRIVATE_KEY",
    "ARC_RPC_URL",
    "ARC_CHAIN_ID",
  ];

  for (const key of required) {
    if (!process.env[key]) {
      throw new Error(`❌ Missing required environment variable: ${key}`);
    }
  }

  console.log("✅ All required variables present");
  console.log(`   - PRIVATE_KEY: ${process.env.PRIVATE_KEY.slice(0, 6)}...${process.env.PRIVATE_KEY.slice(-4)}`);
  console.log(`   - ARC_RPC_URL: ${process.env.ARC_RPC_URL}`);
  console.log(`   - ARC_CHAIN_ID: ${process.env.ARC_CHAIN_ID}\n`);
}

async function validateNetwork() {
  console.log("🌐 Validating network connection...\n");

  try {
    const chainId = await ethers.provider.getNetwork();
    console.log(`✅ Connected to network: ${chainId.name} (Chain ID: ${chainId.chainId})`);

    const blockNumber = await ethers.provider.getBlockNumber();
    console.log(`✅ Latest block: ${blockNumber}\n`);

    return true;
  } catch (error) {
    console.error(`❌ Network validation failed: ${error.message}`);
    return false;
  }
}

async function validateAccount() {
  console.log("👤 Validating account...\n");

  try {
    const [deployer] = await ethers.getSigners();
    const balance = await ethers.provider.getBalance(deployer.address);

    console.log(`✅ Deployer address: ${deployer.address}`);
    console.log(`✅ Account balance: ${ethers.utils.formatEther(balance)} ETH\n`);

    if (balance.isZero()) {
      console.warn("⚠️  WARNING: Account has zero balance. Deployment will fail.");
      return false;
    }

    return true;
  } catch (error) {
    console.error(`❌ Account validation failed: ${error.message}`);
    return false;
  }
}

async function deployContract() {
  console.log("📤 Deploying contract...\n");

  try {
    const [deployer] = await ethers.getSigners();

    // Compile
    console.log("🔨 Compiling...");
    await hre.run("compile");

    // Deploy
    console.log("⏳ Deploying Orvion contract...");
    const Orvion = await ethers.getContractFactory("Orvion");
    const orvion = await Orvion.deploy();
    await orvion.deployed();

    console.log(`✅ Contract deployed at: ${orvion.address}\n`);

    return orvion.address;
  } catch (error) {
    console.error(`❌ Deployment failed: ${error.message}`);
    throw error;
  }
}

async function saveDeployment(contractAddress) {
  console.log("💾 Saving deployment info...\n");

  const [deployer] = await ethers.getSigners();
  const chainId = await ethers.provider.getNetwork();

  const deploymentInfo = {
    network: "arc-testnet",
    chainId: chainId.chainId,
    address: contractAddress,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    blockNumber: await ethers.provider.getBlockNumber(),
    version: "2.0.0",
  };

  const filename = `./deployments/arc-testnet-${Date.now()}.json`;
  fs.writeFileSync(filename, JSON.stringify(deploymentInfo, null, 2));

  console.log(`✅ Deployment info saved to: ${filename}`);

  // Also update main deployment file
  fs.writeFileSync(
    "./deployments/arc-testnet.json",
    JSON.stringify(deploymentInfo, null, 2)
  );

  console.log(`✅ Updated: ./deployments/arc-testnet.json\n`);

  return deploymentInfo;
}

async function verifyDeployment(contractAddress) {
  console.log("🔍 Verifying deployment...\n");

  try {
    const code = await ethers.provider.getCode(contractAddress);

    if (code === "0x") {
      console.error("❌ Contract not found at address");
      return false;
    }

    console.log(`✅ Contract verified at: ${contractAddress}`);
    console.log(`✅ Bytecode length: ${code.length} bytes\n`);

    return true;
  } catch (error) {
    console.error(`❌ Verification failed: ${error.message}`);
    return false;
  }
}

async function main() {
  try {
    console.log("\n╔════════════════════════════════════════════╗");
    console.log("║  ORVION Smart Contract Secure Deployment  ║");
    console.log("╚════════════════════════════════════════════╝\n");

    // Validation
    await validateEnvironment();
    const networkOk = await validateNetwork();
    const accountOk = await validateAccount();

    if (!networkOk || !accountOk) {
      throw new Error("Validation failed. Please check your configuration.");
    }

    // Deploy
    const contractAddress = await deployContract();

    // Save
    const deployment = await saveDeployment(contractAddress);

    // Verify
    const verified = await verifyDeployment(contractAddress);

    if (!verified) {
      throw new Error("Contract verification failed");
    }

    console.log("╔════════════════════════════════════════════╗");
    console.log("║        ✅ DEPLOYMENT SUCCESSFUL ✅         ║");
    console.log("╚════════════════════════════════════════════╝\n");

    console.log("Deployment Summary:");
    console.log(`  Network: ${deployment.network}`);
    console.log(`  Chain ID: ${deployment.chainId}`);
    console.log(`  Contract: ${deployment.address}`);
    console.log(`  Deployer: ${deployment.deployer}`);
    console.log(`  Timestamp: ${deployment.timestamp}\n`);

    process.exit(0);
  } catch (error) {
    console.error("\n❌ DEPLOYMENT FAILED");
    console.error(`Error: ${error.message}\n`);
    process.exit(1);
  }
}

main();
