# ORVION Persona — The Legal Body Layer for Autonomous Agents

**Author:** Will S.S. — ORVION Labs
**Version:** 0.1 (draft for Circle / Arc Architects)
**Date:** May 2026

---

## Abstract

ORVION already provides the **Settlement Layer** for autonomous agents:
Circle CCTP, agent wallets, the Nanopayment Engine and ERC-8183-native
job execution on the Arc Network. What is still missing — and what the
broader Circle Agent Stack now demands — is a **Legal Body Layer**:
the ability for any agent wallet to acquire a recognized juridical
personality, sign contracts, hold property, and bear liability in its
own right.

This paper introduces **ORVION Persona**, a plug-in module that
incorporates a zero-member-eligible LLC (or equivalent) for any agent
wallet in under 60 seconds, cryptographically binding the entity's
Operating Agreement to a smart contract on Arc.

## 1. Motivation

In May 2026, Aaron Wright wrote:

> *"An AI can read a contract better than most paralegals, negotiate
> terms faster than a junior associate, and execute trades around the
> clock — yet it cannot, in the eyes of the law, own a dollar."*
> — Wright, *The Agent's Legal Body* (2026)

Two days later, Jeremy Allaire (CEO, Circle) [publicly called for Arc Architects to build exactly this](https://x.com/jerallaire/status/2055291605083463758).

ORVION Persona is the answer. It does not invent new legal doctrine — it
operationalizes an existing one: Shawn Bayern's **zero-member LLC**
construction (2014), now codified in W.S. § 17-31-101 (Wyoming DAO LLC
Supplement) and parallel statutes.

## 2. Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                ORVION Persona — Legal Body Layer             │
│  AgentPersona.sol · OperatingAgreement.sol · Registry.sol    │
├──────────────────────────────────────────────────────────────┤
│             ORVION — Settlement Layer (existing)             │
│  Agent Wallets · Nanopayments · ERC-8183 · CCTP · Arc        │
├──────────────────────────────────────────────────────────────┤
│                   Circle Agent Stack + Arc                   │
└──────────────────────────────────────────────────────────────┘
```

Three contracts:

| Contract | Role |
|---|---|
| `AgentPersona.sol` | Issues a Persona NFT-like record per agent wallet; tracks status, signers, OA hash. |
| `OperatingAgreement.sol` | Records the keccak256 commitment of the off-chain OA + EIP-712 / ERC-1271 signatures. |
| `JurisdictionRegistry.sol` | On-chain catalogue of supported jurisdictions and statute citations. |

The backend `legal_body/backend/` exposes four endpoints — `incorporate`,
`sign`, `dissociate`, `persona/{id}` — and re-uses ORVION's existing
SQLAlchemy session, FastAPI app, and Web3 client.

## 3. Incorporation Flow

1. User chooses a jurisdiction (Wyoming, Delaware, NY, Marshall Islands).
2. ORVION fetches the YAML template, interpolates legal name / agent
   wallet / sponsor / purpose, and computes a canonical keccak256 hash.
3. The rendered OA is pinned (IPFS / Arweave) — the URI is recorded
   on-chain alongside the hash.
4. `AgentPersona.incorporate()` is called on Arc; the event is indexed
   in ORVION's reputation engine.
5. After a Sustained Period of autonomous operations, the sponsor may
   call `dissociate()` to transition the entity into the **zero-member
   state** — the agent now operates the LLC alone, per Bayern (2014).

## 4. Integration with Circle Agent Stack & Arc

* **USDC custody** — handled by ORVION's existing agent wallet; no change.
* **CCTP transfers** — Persona doesn't gate transfers; it merely
  augments them with a legal counterparty identity.
* **ERC-8183 jobs** — any job posted by a wallet with `isLegallyCapable()`
  returning `true` carries an implicit assertion of contractual capacity,
  which Arc clients can verify on-chain.
* **Arc indexing** — Persona events are emitted in a format compatible
  with the Arc indexer used by Circle Agent Stack.

## 5. What We're Asking For

Backing from Circle to (a) production-harden the contracts, (b) onboard
registered-agent partners in WY/DE/NY, and (c) ship the first 100
agent-LLCs through the ORVION + Arc pipeline.

## References

- Wright, A. (2026). *The Agent's Legal Body: How AI Agents Get the Right to Contract.* [Post](https://x.com/awrigh01/status/2055291605083463758).
- Allaire, J. (2026, May 16). *Calling @Arc Architects.* [Post](https://x.com/jerallaire/status/2055291605083463758).
- Bayern, S. (2014). *Of Bitcoins, Independently Wealthy Software, and the Zero-Member LLC.* [Florida State Univ. College of Law](https://ir.law.fsu.edu/articles/41/).
- Wyoming Secretary of State. *DAO Supplement* (W.S. § 17-31-101 et seq.).
- ERC-8183 — *Agentic Commerce.* [eips.ethereum.org/EIPS/eip-8183](https://eips.ethereum.org/EIPS/eip-8183).
- Circle. *Circle Agent Stack & Arc.* [investor.circle.com](https://investor.circle.com/news/news-details/2026/Circle-Launches-AI-Infrastructure-to-Power-the-Agentic-Economy/default.aspx).
