/**
 * ORVION Agent Workflow Example
 * 
 * Demonstrates a complete agent lifecycle:
 * 1. Register agent
 * 2. Poll for available jobs
 * 3. Complete jobs with proof
 * 4. Track earnings and reputation
 */

import { OrvionClient } from '@orvion/sdk';

interface AgentConfig {
  address: string;
  name: string;
  type: string;
  capabilities: string[];
  pricingPerCall: number;
}

class OrvionAgent {
  private client: OrvionClient;
  private config: AgentConfig;
  private agentId: string = '';
  private earnings: number = 0;
  private jobsCompleted: number = 0;

  constructor(config: AgentConfig, apiToken?: string) {
    this.config = config;
    this.client = new OrvionClient({
      baseUrl: process.env.ORVION_API_URL || 'http://localhost:8000',
      apiToken: apiToken || process.env.ORVION_API_KEY,
      logLevel: 'info'
    });
  }

  /**
   * Register the agent in ORVION Discovery Registry
   */
  async register(): Promise<void> {
    console.log(`📝 Registering agent: ${this.config.name}`);

    const agent = await this.client.registerAgent({
      agent_address: this.config.address,
      agent_name: this.config.name,
      agent_type: this.config.type,
      capabilities: this.config.capabilities,
      pricing_per_call: this.config.pricingPerCall,
      endpoint_url: process.env.AGENT_ENDPOINT_URL,
      settlement_address: this.config.address
    });

    this.agentId = agent.id;
    console.log(`✅ Agent registered: ${this.agentId}`);
  }

  /**
   * Poll for available jobs and process them
   */
  async startWorking(durationSeconds: number = 60): Promise<void> {
    console.log(`🚀 Agent starting work loop (${durationSeconds}s)`);

    const startTime = Date.now();
    const endTime = startTime + (durationSeconds * 1000);

    while (Date.now() < endTime) {
      try {
        // In a real scenario, this would poll an actual job queue
        console.log(`⏳ Polling for jobs...`);

        // Simulate job processing
        await this.processSimulatedJob();

        // Wait before next poll
        await new Promise(resolve => setTimeout(resolve, 5000));

      } catch (error) {
        console.error('❌ Error during work cycle:', error);
        // Continue working despite errors
      }
    }

    console.log(`⏹️  Agent work loop completed`);
  }

  /**
   * Process a simulated job
   */
  private async processSimulatedJob(): Promise<void> {
    const jobId = `job-${Date.now()}`;
    const amount = this.config.pricingPerCall;

    try {
      // Create job and escrow
      console.log(`📦 Creating job: ${jobId} (amount: ${amount} USDC)`);

      const settlement = await this.client.createJobAndEscrow({
        agent_id: this.agentId,
        job_id: jobId,
        amount: amount,
        to_address: this.config.address
      });

      console.log(`✅ Job created: ${settlement.id}`);

      // Simulate work
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Generate proof of work (in real scenario, this would be actual computation)
      const proof = this.generateProof(jobId);

      // Submit proof
      console.log(`📤 Submitting proof for job: ${jobId}`);

      const receipt = await this.client.submitProofOfWork({
        job_id: jobId,
        proof: proof
      });

      console.log(`✅ Proof submitted: ${receipt.id}`);

      // Check settlement status
      const status = await this.client.getStatus(settlement.id);
      console.log(`📊 Settlement status: ${status.status}`);

      // Update stats
      this.earnings += amount;
      this.jobsCompleted += 1;

      console.log(`💰 Earnings: ${this.earnings} USDC | Jobs: ${this.jobsCompleted}`);

    } catch (error: any) {
      console.error(`❌ Failed to process job ${jobId}:`, error.message);
    }
  }

  /**
   * Generate proof of work (simulated)
   */
  private generateProof(jobId: string): string {
    // In a real scenario, this would be actual computation result
    const hash = Buffer.from(jobId + Date.now()).toString('hex');
    return `Qm${hash.substring(0, 44)}`;
  }

  /**
   * Get agent reputation and statistics
   */
  async getStats(): Promise<void> {
    try {
      const reputation = await this.client.getAgentReputation(this.agentId);

      console.log(`\n📊 Agent Statistics:`);
      console.log(`  Agent ID: ${this.agentId}`);
      console.log(`  Reputation Score: ${reputation.score}/5`);
      console.log(`  Total Jobs: ${reputation.total_jobs}`);
      console.log(`  Success Rate: ${(reputation.success_rate * 100).toFixed(2)}%`);
      console.log(`  Average Rating: ${reputation.average_rating.toFixed(2)}/5`);
      console.log(`  Earnings: ${this.earnings} USDC`);
      console.log(`  Jobs Completed: ${this.jobsCompleted}\n`);

    } catch (error: any) {
      console.error('❌ Failed to get stats:', error.message);
    }
  }

  /**
   * Shutdown the agent gracefully
   */
  async shutdown(): Promise<void> {
    console.log(`\n🛑 Shutting down agent...`);
    await this.getStats();
    this.client.close();
    console.log(`✅ Agent shutdown complete`);
  }
}

/**
 * Main entry point
 */
async function main() {
  const agentConfig: AgentConfig = {
    address: process.env.AGENT_WALLET || '0x1234567890123456789012345678901234567890',
    name: process.env.AGENT_NAME || 'DataProcessor-01',
    type: 'processor',
    capabilities: ['data_processing', 'validation', 'analysis'],
    pricingPerCall: 0.5
  };

  const agent = new OrvionAgent(agentConfig);

  try {
    // Register agent
    await agent.register();

    // Start working
    await agent.startWorking(60); // Work for 60 seconds

    // Get final stats
    await agent.getStats();

  } catch (error) {
    console.error('❌ Fatal error:', error);
    process.exit(1);

  } finally {
    await agent.shutdown();
  }
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}

export { OrvionAgent };
