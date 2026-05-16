import { OrvionClient } from '@orvion/sdk';

async function runAgent() {
  const client = new OrvionClient({
    apiKey: process.env.ORVION_API_KEY,
    network: 'arc-testnet'
  });

  console.log('🤖 Starting ORVION Agent...');

  const agent = await client.agents.register({
    name: 'DataProcessor-001',
    walletAddress: process.env.AGENT_WALLET,
    capabilities: ['data_processing', 'ml_inference']
  });

  console.log(`✓ Agent registered: ${agent.agent_id}`);

  let jobsProcessed = 0;
  let totalEarnings = 0;

  while (true) {
    const jobs = await client.jobs.getAvailable({
      capabilities: ['data_processing'],
      limit: 5
    });

    for (const job of jobs) {
      console.log(`📋 Processing job: ${job.job_id}`);
      
      const completed = await client.jobs.complete(job.job_id, {
        proof: `Qm${Math.random().toString(36).substr(2, 44)}`
      });

      const settlement = await client.jobs.settle(job.job_id);
      console.log(`✓ Settled: ${settlement.amount_usdc} USDC`);

      jobsProcessed++;
      totalEarnings += job.amount_usdc;
    }

    console.log(`📈 Stats: ${jobsProcessed} jobs, ${totalEarnings} USDC earned`);
    await new Promise(r => setTimeout(r, 5000));
  }
}

runAgent().catch(console.error);
