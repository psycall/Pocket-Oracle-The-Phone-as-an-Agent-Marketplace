# `tests/` - Integration and Unit Tests

This directory contains all the test suites for the ORVION project, ensuring the reliability and correctness of its functionalities. Tests are crucial for validating both the off-chain business logic and the on-chain interactions with smart contracts.

## Contents

*   `test_settlement_integration.py`: Integration tests specifically designed to validate the end-to-end on-chain settlement lifecycle, including `createJob`, `completeJob`, `settleJob`, and USDC approval mechanisms. These tests simulate real blockchain interactions (using mocks for `Web3.py` to avoid actual network calls during local testing).
*   Other test files (if applicable) for unit tests of individual modules, API endpoints, or utility functions.

## Running Tests

To execute the test suite, navigate to the project root and run:

```bash
python -m unittest discover tests
```

### Important Considerations for Testing:

*   **Environment Variables**: Ensure your `.env` file (or environment variables) is correctly configured with test-specific values. This includes RPC URLs, contract addresses, and especially **test private keys**.
*   **Test Private Keys**: **NEVER** use your production or main wallet private keys for testing. Always generate dedicated test private keys for your testing environment. This is a critical security measure to prevent accidental loss of funds or compromise of your main assets.
*   **Mocking**: For integration tests involving blockchain interactions, `Web3.py` calls are often mocked to simulate transaction outcomes without incurring gas costs or waiting for block confirmations. This allows for faster and more deterministic testing.

## Adding New Tests

When adding new features or modifying existing logic, it is imperative to write corresponding tests. This practice helps maintain code quality, prevents regressions, and ensures that the system behaves as expected under various conditions.

---

*Copyright © 2026 ORVION. All rights reserved.*
