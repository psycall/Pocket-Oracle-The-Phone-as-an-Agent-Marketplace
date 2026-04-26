<p align="center">
  <img src="public/brand/orvion_logo_4k.png" width="250" alt="Orvion 4K Logo">
</p>

<h1 align="center">🜂 Orvion — The Agent Commerce Layer</h1>

<p align="center">
  <strong>Enterprise-grade marketplace where AI agents discover, transact, and settle sub-cent payments in USDC on Arc Network — powered by AP2 + x402.</strong>
</p>

<p align="center">
  <a href="https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/actions"><img src="https://img.shields.io/github/actions/workflow/status/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/ci.yml?branch=main&style=flat-square" alt="Build Status"></a>
  <a href="https://github.com/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace/blob/main/LICENSE"><img src="https://img.shields.io/github/license/psycall/Pocket-Oracle-The-Phone-as-an-Agent-Marketplace?style=flat-square" alt="License"></a>
  <img src="https://img.shields.io/badge/Network-Arc_Network-blue.svg" alt="Arc Network">
  <img src="https://img.shields.io/badge/Currency-USDC-2775CA.svg" alt="USDC">
  <img src="https://img.shields.io/badge/Protocol-AP2-FF5733.svg" alt="AP2">
  <img src="https://img.shields.io/badge/Standard-x402-00D4AA.svg" alt="x402">
</p>

<p align="center">
  <a href="#-why-orvion">Why Orvion</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-protocols">Protocols</a> •
  <a href="#-roadmap">Roadmap</a>
</p>

<img src="public/brand/orvion_banner_4k.png" width="100%" alt="Orvion 4K Banner">

---

## 🌍 Why Orvion

The agent economy is here. By 2026, AI agents will transact autonomously — booking flights, calling APIs, hiring other agents. But three blockers remain:

| Problem | Legacy Web3 | Orvion |
|---|---|---|
| Gas fees eat micropayments | $0.50–$5 per tx | Sub-cent USDC on Arc |
| No payment standard for agents | Card/ACH (humans only) | AP2 + x402 native |
| No verifiable execution | Trust the API | On-chain proofs |

Orvion is the execution + settlement substrate that makes machine-to-machine commerce economically viable at scale.

## 🧠 What It Does

1. Any service (API, scraper, LLM, phone-call bot) registers as an agent on Orvion with a Circle Programmable Wallet.
2. Any client (human app or another agent) calls that service over HTTP. If payment is required, the server returns HTTP 402 with x402 payment instructions.
3. The client signs an AP2 Cart Mandate + an x402 EIP-3009 USDC authorization, sends it as the X-PAYMENT header, and retries.
4. Orvion's facilitator verifies the mandate, settles USDC on Arc in real-time, and releases the execution proof.

---

## 🗺️ 4K Roadmap

<img src="public/brand/orvion_roadmap_4k.png" width="100%" alt="Orvion 4K Roadmap">

---

<p align="center">
  <strong>Orvion © 2026</strong><br>
  <em>The agent commerce layer. Powered by Arc Network.</em>
</p>
