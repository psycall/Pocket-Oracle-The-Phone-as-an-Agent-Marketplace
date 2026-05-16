const hre = require("hardhat");
const fs = require("fs");
require("dotenv").config();

async function main() {
  console.log("🚀 Iniciando deploy do contrato Orvion em Arc testnet...\n");

  // Obter signer
  const [deployer] = await ethers.getSigners();
  console.log(`📝 Deploying com conta: ${deployer.address}`);

  // Compilar contrato
  console.log("\n🔨 Compilando contrato...");
  await hre.run("compile");

  // Deploy
  console.log("📤 Fazendo deploy...");
  const Orvion = await ethers.getContractFactory("Orvion");
  // Endereço USDC fictício para teste local ou endereço real se disponível
  const usdcAddress = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"; // Exemplo USDC Polygon
  const orvion = await Orvion.deploy(usdcAddress);
  await orvion.waitForDeployment();
  const orvionAddress = await orvion.getAddress();

  console.log(`\n✅ Contrato deployado em: ${orvionAddress}`);

  // Salvar endereço
  const deploymentInfo = {
    network: "arc-testnet",
    address: orvionAddress,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    blockNumber: await ethers.provider.getBlockNumber(),
  };

  fs.writeFileSync(
    "./deployments/arc-testnet.json",
    JSON.stringify(deploymentInfo, null, 2)
  );

  console.log("📁 Deployment info salvo em deployments/arc-testnet.json");

  // Verificar contrato
  console.log("\n🔍 Verificando contrato...");
  try {
    const code = await ethers.provider.getCode(orvionAddress);
    console.log(`✅ Contrato verificado. Bytecode length: ${code.length}`);
  } catch (error) {
    console.error("❌ Erro ao verificar contrato:", error.message);
  }

  console.log("\n🎉 Deploy concluído com sucesso!");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
