// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title AgentPersona
 * @author Will S.S. (ORVION Labs)
 * @notice On-chain registry for AI Agent Legal Personas.
 *         Each persona represents a zero-member LLC (or equivalent) tied to an
 *         autonomous agent wallet — granting the agent the right to contract,
 *         hold property, sue and be sued under U.S. business-entity codes.
 *
 *         Theoretical foundation:
 *         - Bayern (2014) "Of Bitcoins, Independently Wealthy Software, and the
 *           Zero-Member LLC"
 *         - Wyoming DAO LLC Supplement (W.S. 17-31-101 et seq.)
 *         - Aaron Wright (2026) "The Agent's Legal Body"
 *
 *         Designed to plug directly into ORVION's existing Agent Wallet system
 *         and ERC-8183 job lifecycle.
 */

interface IAgentWallet {
    function owner() external view returns (address);
}

contract AgentPersona {
    // ───────────────────────────── ENUMS ─────────────────────────────
    enum Jurisdiction { WYOMING_DAO_LLC, DELAWARE_SERIES_LLC, NEW_YORK_LLC, MARSHALL_ISLANDS_DAO }
    enum Status { PENDING, INCORPORATED, SUSPENDED, DISSOLVED }

    // ───────────────────────────── STRUCT ────────────────────────────
    struct Persona {
        uint256 id;
        address agentWallet;          // ORVION Agent Wallet bound to this persona
        address humanSponsor;         // Initial sponsor (can be address(0) once autonomous)
        Jurisdiction jurisdiction;
        Status status;
        string legalName;             // e.g. "Orion Trading Agent LLC"
        bytes32 operatingAgreementHash; // keccak256 of the YAML/JSON Operating Agreement
        string registeredAgentURI;    // IPFS/URI to registered agent contact
        uint64 incorporatedAt;
        uint64 lastUpdatedAt;
    }

    // ─────────────────────────── STORAGE ─────────────────────────────
    uint256 public nextPersonaId = 1;
    mapping(uint256 => Persona) public personas;
    mapping(address => uint256) public walletToPersona; // agentWallet -> personaId
    mapping(uint256 => mapping(address => bool)) public authorizedSigners;

    address public immutable jurisdictionRegistry;
    address public governance;

    // ─────────────────────────── EVENTS ──────────────────────────────
    event PersonaIncorporated(uint256 indexed id, address indexed agentWallet, Jurisdiction j, string legalName);
    event OperatingAgreementSigned(uint256 indexed id, bytes32 agreementHash, address signer);
    event PersonaDissociated(uint256 indexed id, string reason);
    event StatusChanged(uint256 indexed id, Status from, Status to);
    event AuthorizedSignerAdded(uint256 indexed id, address signer);

    // ────────────────────────── MODIFIERS ────────────────────────────
    modifier onlyGovernance() {
        require(msg.sender == governance, "AgentPersona: not governance");
        _;
    }

    modifier onlyAuthorized(uint256 personaId) {
        require(
            msg.sender == personas[personaId].humanSponsor ||
            msg.sender == personas[personaId].agentWallet ||
            authorizedSigners[personaId][msg.sender],
            "AgentPersona: unauthorized"
        );
        _;
    }

    // ───────────────────────── CONSTRUCTOR ───────────────────────────
    constructor(address _jurisdictionRegistry) {
        jurisdictionRegistry = _jurisdictionRegistry;
        governance = msg.sender;
    }

    // ─────────────────────── CORE FUNCTIONS ──────────────────────────

    /**
     * @notice Incorporates a new legal persona for an agent wallet.
     * @dev    The caller becomes the initial humanSponsor. Once the OA is
     *         executed and the agent demonstrates autonomy, sponsor can be
     *         zeroed out via `dissociate()` — making the entity a true
     *         zero-member LLC (Bayern model).
     */
    function incorporate(
        address agentWallet,
        Jurisdiction j,
        string calldata legalName,
        bytes32 operatingAgreementHash,
        string calldata registeredAgentURI
    ) external returns (uint256 id) {
        require(agentWallet != address(0), "AgentPersona: wallet=0");
        require(walletToPersona[agentWallet] == 0, "AgentPersona: already incorporated");
        require(bytes(legalName).length > 0, "AgentPersona: empty name");

        id = nextPersonaId++;
        personas[id] = Persona({
            id: id,
            agentWallet: agentWallet,
            humanSponsor: msg.sender,
            jurisdiction: j,
            status: Status.INCORPORATED,
            legalName: legalName,
            operatingAgreementHash: operatingAgreementHash,
            registeredAgentURI: registeredAgentURI,
            incorporatedAt: uint64(block.timestamp),
            lastUpdatedAt: uint64(block.timestamp)
        });
        walletToPersona[agentWallet] = id;
        authorizedSigners[id][msg.sender] = true;
        authorizedSigners[id][agentWallet] = true;

        emit PersonaIncorporated(id, agentWallet, j, legalName);
    }

    /**
     * @notice Records execution of (or amendment to) the Operating Agreement.
     */
    function signOperatingAgreement(uint256 personaId, bytes32 newHash)
        external
        onlyAuthorized(personaId)
    {
        Persona storage p = personas[personaId];
        require(p.status == Status.INCORPORATED, "AgentPersona: not active");
        p.operatingAgreementHash = newHash;
        p.lastUpdatedAt = uint64(block.timestamp);
        emit OperatingAgreementSigned(personaId, newHash, msg.sender);
    }

    /**
     * @notice Removes the human sponsor, achieving the zero-member configuration.
     *         Per Bayern (2014), the LLC continues to exist with no members —
     *         the agent wallet now operates the entity autonomously.
     */
    function dissociate(uint256 personaId, string calldata reason)
        external
        onlyAuthorized(personaId)
    {
        Persona storage p = personas[personaId];
        require(p.humanSponsor != address(0), "AgentPersona: already zero-member");
        p.humanSponsor = address(0);
        p.lastUpdatedAt = uint64(block.timestamp);
        emit PersonaDissociated(personaId, reason);
    }

    function addAuthorizedSigner(uint256 personaId, address signer)
        external
        onlyAuthorized(personaId)
    {
        authorizedSigners[personaId][signer] = true;
        emit AuthorizedSignerAdded(personaId, signer);
    }

    function setStatus(uint256 personaId, Status s) external onlyGovernance {
        Status prev = personas[personaId].status;
        personas[personaId].status = s;
        personas[personaId].lastUpdatedAt = uint64(block.timestamp);
        emit StatusChanged(personaId, prev, s);
    }

    // ─────────────────────────── VIEWS ───────────────────────────────
    function getPersonaByWallet(address agentWallet) external view returns (Persona memory) {
        uint256 id = walletToPersona[agentWallet];
        require(id != 0, "AgentPersona: none");
        return personas[id];
    }

    function isLegallyCapable(address agentWallet) external view returns (bool) {
        uint256 id = walletToPersona[agentWallet];
        if (id == 0) return false;
        return personas[id].status == Status.INCORPORATED;
    }
}
