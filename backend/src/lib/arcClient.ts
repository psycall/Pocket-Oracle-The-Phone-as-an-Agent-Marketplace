import { ethers } from 'ethers';

const ARC_CHAIN_ID = Number(process.env.ARC_CHAIN_ID ?? 5042002);
const ARC_RPC      = process.env.ARC_RPC_URL ?? 'https://rpc.testnet.arc.network';
const USDC_ADDR    = process.env.USDC_CONTRACT_ADDRESS ?? '0x3600000000000000000000000000000000000000';

const REGISTRY_ABI = [
  'function register(address,bytes32,bytes32) external',
  'function getAgent(address) view returns (tuple(address owner,address agentWallet,bytes32 capabilitiesHash,bytes32 ap2DidHash,uint256 reputation,uint256 totalTasksCompleted,uint256 totalEarnedUSDC,uint64 registeredAt,bool active))',
  'function isRegistered(address) view returns (bool)',
  'function totalAgents() view returns (uint256)',
];

const ESCROW_ABI = [
  'function createTask(bytes32,address,uint256,bytes32,bytes32,uint64) external',
  'function completeTask(bytes32,bytes32) external',
  'function refund(bytes32) external',
  'function tasks(bytes32) view returns (tuple(bytes32 id,address requester,address executor,uint256 amount,bytes32 inputHash,bytes32 cartMandateHash,bytes32 outputHash,uint64 createdAt,uint64 deadline,uint8 status))',
];

const PROOF_ABI = [
  'function anchor(bytes32,bytes32,bytes32) external',
  'function receipts(bytes32) view returns (tuple(bytes32 taskId,address executor,bytes32 paymentMandateHash,bytes32 outputHash,uint64 timestamp))',
];

const USDC_ABI = [
  'function balanceOf(address) view returns (uint256)',
  'function transfer(address,uint256) returns (bool)',
  'function transferWithAuthorization(address,address,uint256,uint256,uint256,bytes32,uint8,bytes32,bytes32) external',
];

export class ArcClient {
  readonly provider: ethers.JsonRpcProvider;
  readonly signer: ethers.Wallet;
  readonly registry: ethers.Contract;
  readonly escrow: ethers.Contract;
  readonly proof: ethers.Contract;
  readonly usdc: ethers.Contract;

  constructor() {
    this.provider = new ethers.JsonRpcProvider(ARC_RPC, {
      chainId: ARC_CHAIN_ID,
      name: 'arc-testnet',
    });
    this.signer   = new ethers.Wallet(process.env.ARC_PRIVATE_KEY!, this.provider);
    this.registry = new ethers.Contract(process.env.AGENT_REGISTRY_ADDRESS!,    REGISTRY_ABI, this.signer);
    this.escrow   = new ethers.Contract(process.env.TASK_ESCROW_ADDRESS!,       ESCROW_ABI,   this.signer);
    this.proof    = new ethers.Contract(process.env.PROOF_OF_EXECUTION_ADDRESS!, PROOF_ABI,   this.signer);
    this.usdc     = new ethers.Contract(USDC_ADDR, USDC_ABI, this.signer);
  }

  hashPayload(payload: unknown): string {
    return ethers.keccak256(ethers.toUtf8Bytes(JSON.stringify(payload)));
  }
}

export const arcClient = new ArcClient();
