// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title OperatingAgreement
 * @notice Stores cryptographic commitments to off-chain Operating Agreements
 *         (YAML/JSON in IPFS or Arweave) and tracks multi-party execution.
 *         Compatible with EIP-712 typed signatures for human signatories
 *         and ERC-1271 for agent (contract-wallet) signatures.
 */
contract OperatingAgreement {
    struct Agreement {
        uint256 personaId;
        bytes32 documentHash;     // keccak256 of canonical YAML
        string  documentURI;      // ipfs://... or ar://...
        uint64  effectiveAt;
        uint64  amendedAt;
        address[] signatories;
    }

    mapping(uint256 => Agreement) public agreements; // personaId -> latest agreement
    mapping(uint256 => mapping(address => bytes)) public signatures;

    event AgreementRegistered(uint256 indexed personaId, bytes32 documentHash, string uri);
    event AgreementSigned(uint256 indexed personaId, address indexed signer);
    event AgreementAmended(uint256 indexed personaId, bytes32 newHash, string newURI);

    function register(
        uint256 personaId,
        bytes32 documentHash,
        string calldata documentURI,
        address[] calldata signatories
    ) external {
        Agreement storage a = agreements[personaId];
        a.personaId = personaId;
        a.documentHash = documentHash;
        a.documentURI = documentURI;
        a.effectiveAt = uint64(block.timestamp);
        a.signatories = signatories;
        emit AgreementRegistered(personaId, documentHash, documentURI);
    }

    function sign(uint256 personaId, bytes calldata signature) external {
        signatures[personaId][msg.sender] = signature;
        emit AgreementSigned(personaId, msg.sender);
    }

    function amend(
        uint256 personaId,
        bytes32 newHash,
        string calldata newURI
    ) external {
        Agreement storage a = agreements[personaId];
        a.documentHash = newHash;
        a.documentURI = newURI;
        a.amendedAt = uint64(block.timestamp);
        emit AgreementAmended(personaId, newHash, newURI);
    }
}
