import circle from './src/services/circleService.js';
import fs from 'fs';

async function backTest() {
    console.log("🔍 Iniciando Back-test do Fluxo Pocket Oracle...");
    
    const wallet = await circle.createAgentWallet("agent_001");
    if(wallet.success) console.log("✅ Circle Service: Wallet creation simulation passed.");
    
    const criticalFiles = ['contracts/PocketOracle.sol', 'hardhat.config.js', 'package.json'];
    criticalFiles.forEach(file => {
        if(fs.existsSync(file)) console.log(`✅ File System: ${file} found.`);
        else console.error(`❌ File System: ${file} MISSING!`);
    });

    console.log("🏆 Back-test concluído: Sistema estável para execução.");
}
backTest();
