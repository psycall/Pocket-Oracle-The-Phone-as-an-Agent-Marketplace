import { ethers } from 'hardhat';
import fs from 'fs';

async function deployOrvion() {
  console.log('🚀 ORVION Deployment to Arc Testnet\n');
  const wallet = (await ethers.getSigners())[0];
  console.log(`📍 Deployer: ${wallet.address}`);
  
  const Orvion = await ethers.getContractFactory('Orvion');
  const USDC_ARC = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
  
  console.log('⏳ Deploying Orvion...');
  const orvion = await Orvion.deploy(USDC_ARC);
  await orvion.waitForDeployment();
  
  const deployedAddress = await orvion.getAddress();
  console.log(`✓ Deployed to: ${deployedAddress}\n`);
  
  const deployment = {
    network: 'arc-testnet',
    address: deployedAddress,
    usdc: USDC_ARC,
    deployer: wallet.address,
    timestamp: new Date().toISOString()
  };
  
  if (!fs.existsSync('./deployments')) {
    fs.mkdirSync('./deployments', { recursive: true });
  }
  
  fs.writeFileSync('./deployments/arc-testnet.json', JSON.stringify(deployment, null, 2));
  console.log('📄 Deployment saved to deployments/arc-testnet.json');
  console.log('✓ Deployment complete!');
}

deployOrvion().catch(console.error);
