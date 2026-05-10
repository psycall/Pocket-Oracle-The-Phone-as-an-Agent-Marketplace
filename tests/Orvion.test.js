import { expect } from 'chai';
import { ethers } from 'hardhat';

describe('Orvion Settlement Contract', function () {
  let orvion, usdc, owner, agent, client;
  const JOB_AMOUNT = ethers.parseUnits('100', 6);

  beforeEach(async function () {
    [owner, agent, client] = await ethers.getSigners();
    const ERC20Mock = await ethers.getContractFactory('ERC20Mock');
    usdc = await ERC20Mock.deploy('USD Coin', 'USDC', 6);
    const Orvion = await ethers.getContractFactory('Orvion');
    orvion = await Orvion.deploy(await usdc.getAddress());
    await usdc.mint(client.address, ethers.parseUnits('1000', 6));
    await usdc.connect(client).approve(await orvion.getAddress(), ethers.parseUnits('1000', 6));
  });

  it('Should create a job with correct parameters', async function () {
    const jobHash = ethers.id('test-job-1');
    await orvion.connect(client).createJob(agent.address, JOB_AMOUNT, jobHash);
    const job = await orvion.jobs(0);
    expect(job.creator).to.equal(client.address);
    expect(job.worker).to.equal(agent.address);
    expect(job.amount).to.equal(JOB_AMOUNT);
    expect(job.status).to.equal(1);
  });

  it('Should allow worker to complete job', async function () {
    const jobHash = ethers.id('test-job-2');
    await orvion.connect(client).createJob(agent.address, JOB_AMOUNT, jobHash);
    await orvion.connect(agent).completeJob(0);
    const job = await orvion.jobs(0);
    expect(job.status).to.equal(2);
  });

  it('Should settle payment to worker', async function () {
    const jobHash = ethers.id('test-job-3');
    await orvion.connect(client).createJob(agent.address, JOB_AMOUNT, jobHash);
    await orvion.connect(agent).completeJob(0);
    const agentBalanceBefore = await usdc.balanceOf(agent.address);
    await orvion.settleJob(0);
    const agentBalanceAfter = await usdc.balanceOf(agent.address);
    expect(agentBalanceAfter - agentBalanceBefore).to.equal(JOB_AMOUNT);
  });
});
