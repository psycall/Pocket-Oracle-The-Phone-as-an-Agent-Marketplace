import hardhat from "hardhat";
import fs from "fs";
import path from "path";

const { ethers } = hardhat;

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deployer:", deployer.address);
  console.log(
    "Balance :",
    ethers.formatEther(await ethers.provider.getBalance(deployer.address)),
    "ETH"
  );

  const Factory = await ethers.getContractFactory("PocketOracle");
  const contract = await Factory.deploy();
  await contract.waitForDeployment();

  const address = await contract.getAddress();
  console.log("PocketOracle deployed at:", address);

  const out = path.resolve("deployments.json");
  let store = {};
  if (fs.existsSync(out)) {
    try {
      store = JSON.parse(fs.readFileSync(out, "utf8"));
    } catch {}
  }
  const network = hardhat.network.name;
  store[network] = {
    address,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
  };
  fs.writeFileSync(out, JSON.stringify(store, null, 2));
  console.log(`Saved → ${out} (network: ${network})`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
