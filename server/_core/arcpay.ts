import axios, { AxiosInstance } from 'axios';
import { ethers } from 'ethers';
import { logger } from './middleware';

/**
 * ArcPay Integration for ORVION
 * Handles real USDC settlements on Arc Network
 */

interface ArcPayConfig {
  apiUrl: string;
  apiKey: string;
  walletPrivateKey: string;
  arcRpcUrl: string;
}

interface SettlementRequest {
  recipientAddress: string;
  amount: string;
  jobId: number;
  agentId: number;
  metadata?: Record<string, any>;
}

interface SettlementResponse {
  transactionHash: string;
  status: 'pending' | 'confirmed' | 'failed';
  amount: string;
  recipient: string;
  timestamp: number;
  blockNumber?: number;
}

class ArcPayClient {
  private apiClient: AxiosInstance;
  private config: ArcPayConfig;
  private provider: ethers.JsonRpcProvider;
  private wallet: ethers.Wallet;

  constructor(config: ArcPayConfig) {
    this.config = config;

    this.apiClient = axios.create({
      baseURL: config.apiUrl,
      headers: {
        'Authorization': `Bearer ${config.apiKey}`,
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    });

    this.provider = new ethers.JsonRpcProvider(config.arcRpcUrl);
    this.wallet = new ethers.Wallet(config.walletPrivateKey, this.provider);

    logger.info('ArcPay client initialized', {
      apiUrl: config.apiUrl,
      walletAddress: this.wallet.address,
    });
  }

  async sendSettlement(request: SettlementRequest): Promise<SettlementResponse> {
    try {
      logger.info('Processing ArcPay settlement', {
        recipient: request.recipientAddress,
        amount: request.amount,
        jobId: request.jobId,
      });

      const USDC_ADDRESS = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
      const USDC_ABI = [
        'function transfer(address to, uint256 amount) returns (bool)',
        'function balanceOf(address account) view returns (uint256)',
      ];

      const usdcContract = new ethers.Contract(USDC_ADDRESS, USDC_ABI, this.wallet);
      const amountInWei = ethers.parseUnits(request.amount, 6);

      const balance = await usdcContract.balanceOf(this.wallet.address);
      if (balance < amountInWei) {
        throw new Error(`Insufficient balance. Have: ${balance}, Need: ${amountInWei}`);
      }

      const tx = await usdcContract.transfer(request.recipientAddress, amountInWei);

      logger.info('Settlement transaction sent', {
        txHash: tx.hash,
        recipient: request.recipientAddress,
        amount: request.amount,
      });

      const receipt = await tx.wait();

      const response: SettlementResponse = {
        transactionHash: tx.hash,
        status: receipt?.status === 1 ? 'confirmed' : 'failed',
        amount: request.amount,
        recipient: request.recipientAddress,
        timestamp: Date.now(),
        blockNumber: receipt?.blockNumber,
      };

      logger.info('Settlement confirmed', response);

      return response;
    } catch (error) {
      logger.error('Settlement failed', {
        error: error instanceof Error ? error.message : String(error),
        request,
      });

      throw error;
    }
  }

  async getSettlementStatus(transactionHash: string): Promise<SettlementResponse | null> {
    try {
      const receipt = await this.provider.getTransactionReceipt(transactionHash);

      if (!receipt) {
        return null;
      }

      const tx = await this.provider.getTransaction(transactionHash);

      return {
        transactionHash,
        status: receipt.status === 1 ? 'confirmed' : 'failed',
        amount: ethers.formatUnits(tx?.value || 0, 6),
        recipient: receipt.to || '',
        timestamp: (await this.provider.getBlock(receipt.blockNumber))?.timestamp || Date.now(),
        blockNumber: receipt.blockNumber,
      };
    } catch (error) {
      logger.error('Failed to get settlement status', {
        error: error instanceof Error ? error.message : String(error),
        transactionHash,
      });

      return null;
    }
  }

  async getBalance(): Promise<string> {
    try {
      const USDC_ADDRESS = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
      const USDC_ABI = ['function balanceOf(address account) view returns (uint256)'];

      const usdcContract = new ethers.Contract(USDC_ADDRESS, USDC_ABI, this.provider);
      const balance = await usdcContract.balanceOf(this.wallet.address);

      return ethers.formatUnits(balance, 6);
    } catch (error) {
      logger.error('Failed to get balance', {
        error: error instanceof Error ? error.message : String(error),
      });

      return '0';
    }
  }

  async estimateGasCost(amount: string): Promise<string> {
    try {
      const USDC_ADDRESS = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
      const USDC_ABI = ['function transfer(address to, uint256 amount) returns (bool)'];

      const usdcContract = new ethers.Contract(USDC_ADDRESS, USDC_ABI, this.wallet);
      const amountInWei = ethers.parseUnits(amount, 6);

      const gasEstimate = await usdcContract.transfer.estimateGas(
        this.wallet.address,
        amountInWei
      );

      const feeData = await this.provider.getFeeData();
      const gasPrice = feeData.gasPrice || ethers.parseUnits('1', 'gwei');

      const gasCost = gasEstimate * gasPrice;

      return ethers.formatEther(gasCost);
    } catch (error) {
      logger.error('Failed to estimate gas', {
        error: error instanceof Error ? error.message : String(error),
      });

      return '0.001';
    }
  }
}

let arcPayClient: ArcPayClient | null = null;

export function initializeArcPay(config: ArcPayConfig): ArcPayClient {
  if (!arcPayClient) {
    arcPayClient = new ArcPayClient(config);
  }
  return arcPayClient;
}

export function getArcPayClient(): ArcPayClient {
  if (!arcPayClient) {
    throw new Error('ArcPay client not initialized. Call initializeArcPay first.');
  }
  return arcPayClient;
}

export async function sendSettlement(request: SettlementRequest): Promise<SettlementResponse> {
  const client = getArcPayClient();
  return client.sendSettlement(request);
}

export async function getSettlementStatus(txHash: string): Promise<SettlementResponse | null> {
  const client = getArcPayClient();
  return client.getSettlementStatus(txHash);
}

export async function getWalletBalance(): Promise<string> {
  const client = getArcPayClient();
  return client.getBalance();
}

export async function estimateGasCost(amount: string): Promise<string> {
  const client = getArcPayClient();
  return client.estimateGasCost(amount);
}
