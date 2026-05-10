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
  const orvion = await Orvion.deploy();
  await orvion.deployed();

  console.log(`\n✅ Contrato deployado em: ${orvion.address}`);

  // Salvar endereço
  const deploymentInfo = {
    network: "arc-testnet",
    address: orvion.address,
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
    const code = await ethers.provider.getCode(orvion.address);
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
