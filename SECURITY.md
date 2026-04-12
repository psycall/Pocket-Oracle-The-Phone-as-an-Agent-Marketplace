# Security Policy

## Supported Versions

We take the security of our marketplace and agents seriously. The following versions are currently being supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within Pocket Oracle, please help us by reporting it responsibly. 

**Do not open a public issue for security vulnerabilities.**

Instead, please send an email to security@pocketoracle.ai (simulated) or use the GitHub Private Vulnerability Reporting feature.

### Our Commitment

- We will acknowledge receipt of your report within 48 hours.
- We will provide an estimated timeframe for a fix.
- We will notify you once the vulnerability is patched.

## Security Best Practices for Contributors

- **No Secrets in Code:** Never commit API keys, private keys, or credentials. Use `.env.example` for templates.
- **Dependency Audit:** We use automated tools to scan for vulnerable packages.
- **Least Privilege:** All services and GitHub Actions run with the minimum necessary permissions.
