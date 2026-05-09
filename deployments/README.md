# `deployments/` - Smart Contract Deployment Artifacts

This directory stores the artifacts and records of smart contract deployments for the ORVION project. It is crucial for tracking which contract versions are deployed to which networks and their respective addresses.

## Contents

*   `arc-testnet.json`: Contains the deployment details for the Orvion smart contract on the Arc Testnet. This file typically includes the contract address, ABI, and other metadata generated during the deployment process.
*   Other `.json` files (if applicable) for deployments on different networks (e.g., `ethereum-sepolia.json`, `polygon-mumbai.json`).

## Importance

These deployment artifacts are vital for:

*   **Contract Interaction**: The backend services (e.g., `settlement_engine.py`) use the contract addresses and ABIs from these files to interact with the deployed smart contracts.
*   **Auditing**: Provides a historical record of deployments, which is essential for auditing and verification purposes.
*   **Reproducibility**: Ensures that the correct contract versions and addresses are used across different environments (development, staging, production).

## Security Note

While these files contain public contract addresses and ABIs, they should be managed carefully. Ensure that sensitive information (e.g., private keys used for deployment) is **never** stored within these files or committed to version control.

---

*Copyright © 2026 ORVION. All rights reserved.*
