// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title OrvionEscrow
 * @dev Camada de liquidação para agentes. Retém fundos até validação da tarefa.
 */
contract OrvionEscrow is Ownable, ReentrancyGuard {
    IERC20 public immutable usdcToken;

    struct Settlement {
        address employer;
        address agent;
        uint256 amount;
        bool isReleased;
        bool isDisputed;
        string taskId;
    }

    mapping(bytes32 => Settlement) public settlements;
    mapping(address => uint256) public agentReputation;

    event SettlementCreated(bytes32 indexed settlementId, address employer, address agent, uint256 amount, string taskId);
    event SettlementReleased(bytes32 indexed settlementId, address agent, uint256 amount);
    event SettlementDisputed(bytes32 indexed settlementId);

    constructor(address _usdcToken) Ownable(msg.sender) {
        usdcToken = IERC20(_usdcToken);
    }

    /**
     * @dev Cria uma nova intenção de liquidação.
     */
    function createSettlement(address _agent, uint256 _amount, string memory _taskId) external nonReentrant {
        require(_amount > 0, "Amount must be greater than zero");
        require(usdcToken.transferFrom(msg.sender, address(this), _amount), "Transfer failed");

        bytes32 settlementId = keccak256(abi.encodePacked(msg.sender, _agent, _taskId, block.timestamp));
        
        settlements[settlementId] = Settlement({
            employer: msg.sender,
            agent: _agent,
            amount: _amount,
            isReleased: false,
            isDisputed: false,
            taskId: _taskId
        });

        emit SettlementCreated(settlementId, msg.sender, _agent, _amount, _taskId);
    }

    /**
     * @dev Libera o pagamento para o agente após validação (chamado pelo Oráculo ou Employer).
     */
    function releaseSettlement(bytes32 _settlementId) external nonReentrant {
        Settlement storage s = settlements[_settlementId];
        require(msg.sender == s.employer || msg.sender == owner(), "Not authorized");
        require(!s.isReleased, "Already released");
        require(!s.isDisputed, "Settlement is in dispute");

        s.isReleased = true;
        agentReputation[s.agent] += 1;

        require(usdcToken.transfer(s.agent, s.amount), "Transfer to agent failed");

        emit SettlementReleased(_settlementId, s.agent, s.amount);
    }

    /**
     * @dev Abre uma disputa sobre a liquidação.
     */
    function disputeSettlement(bytes32 _settlementId) external {
        Settlement storage s = settlements[_settlementId];
        require(msg.sender == s.employer || msg.sender == s.agent, "Not authorized");
        require(!s.isReleased, "Already released");

        s.isDisputed = true;
        emit SettlementDisputed(_settlementId);
    }

    /**
     * @dev Resolve disputa (apenas Owner/Admin).
     */
    function resolveDispute(bytes32 _settlementId, bool _refundToEmployer) external onlyOwner nonReentrant {
        Settlement storage s = settlements[_settlementId];
        require(s.isDisputed, "Not in dispute");
        require(!s.isReleased, "Already released");

        s.isReleased = true;
        address recipient = _refundToEmployer ? s.employer : s.agent;
        
        require(usdcToken.transfer(recipient, s.amount), "Resolution transfer failed");
    }
}
