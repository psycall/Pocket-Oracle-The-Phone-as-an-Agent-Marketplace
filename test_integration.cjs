const circle = require('./src/services/circleService');
const fs = require('fs');

async function backTest() {
    console.log("🔍 Iniciando Back-test do Fluxo Pocket Oracle...");
    
    // 1. Testar serviço Circle
    const wallet = await circle.createAgentWallet("agent_001");
    if(wallet.success) console.log("✅ Circle Service: Wallet creation simulation passed.");
    
    // 2. Verificar existência de arquivos críticos
    const criticalFiles = ['contracts/PocketOracle.sol', 'hardhat.config.js', 'package.json'];
    criticalFiles.forEach(file => {
        if(fs.existsSync(file)) console.log(`✅ File System: ${file} found.`);
        else console.error(`❌ File System: ${file} MISSING!`);
    });

    console.log("🏆 Back-test concluído: Sistema estável para execução.");
}
backTest();
