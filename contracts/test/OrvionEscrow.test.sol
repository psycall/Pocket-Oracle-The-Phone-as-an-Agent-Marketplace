// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../OrvionEscrow.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/**
 * @title MockUSDC
 * @dev Mock USDC token for testing
 */
contract MockUSDC is ERC20 {
    constructor() ERC20("USD Coin", "USDC") {
        _mint(msg.sender, 1000000 * 10 ** 6); // 1M USDC
    }

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

/**
 * @title OrvionEscrowTest
 * @dev Comprehensive test suite for OrvionEscrow contract
 */
contract OrvionEscrowTest is Test {
    OrvionEscrow public escrow;
    MockUSDC public usdc;

    address public employer = address(0x1);
    address public agent = address(0x2);
    address public owner = address(0x3);

    uint256 constant SETTLEMENT_AMOUNT = 100 * 10 ** 6; // 100 USDC

    event SettlementCreated(bytes32 indexed settlementId, address employer, address agent, uint256 amount, string taskId);
    event SettlementReleased(bytes32 indexed settlementId, address agent, uint256 amount);
    event SettlementDisputed(bytes32 indexed settlementId);

    function setUp() public {
        // Deploy mock USDC
        usdc = new MockUSDC();

        // Deploy OrvionEscrow
        vm.prank(owner);
        escrow = new OrvionEscrow(address(usdc));

        // Mint USDC to employer
        usdc.mint(employer, 10000 * 10 ** 6); // 10k USDC

        // Approve escrow to spend USDC
        vm.prank(employer);
        usdc.approve(address(escrow), type(uint256).max);
    }

    /**
     * @dev Test: Settlement creation
     */
    function test_CreateSettlement() public {
        vm.prank(employer);
        escrow.createSettlement(agent, SETTLEMENT_AMOUNT, "task-001");

        bytes32 settlementId = keccak256(abi.encodePacked(employer, agent, "task-001", block.timestamp));
        
        (address _employer, address _agent, uint256 amount, bool isReleased, bool isDisputed, string memory taskId) = 
            escrow.settlements(settlementId);

        assertEq(_employer, employer);
        assertEq(_agent, agent);
        assertEq(amount, SETTLEMENT_AMOUNT);
        assertFalse(isReleased);
        assertFalse(isDisputed);
        assertEq(taskId, "task-001");
    }

    /**
     * @dev Test: Settlement release by employer
     */
    function test_ReleaseSettlementByEmployer() public {
        vm.prank(employer);
        escrow.createSettlement(agent, SETTLEMENT_AMOUNT, "task-002");

        bytes32 settlementId = keccak256(abi.encodePacked(employer, agent, "task-002", block.timestamp));

        uint256 agentBalanceBefore = usdc.balanceOf(agent);

        vm.prank(employer);
        escrow.releaseSettlement(settlementId);

        uint256 agentBalanceAfter = usdc.balanceOf(agent);
        assertEq(agentBalanceAfter - agentBalanceBefore, SETTLEMENT_AMOUNT);
    }

    /**
     * @dev Test: Settlement release by owner
     */
    function test_ReleaseSettlementByOwner() public {
        vm.prank(employer);
        escrow.createSettlement(agent, SETTLEMENT_AMOUNT, "task-003");

        bytes32 settlementId = keccak256(abi.encodePacked(employer, agent, "task-003", block.timestamp));

        vm.prank(owner);
        escrow.releaseSettlement(settlementId);

        uint256 agentBalance = usdc.balanceOf(agent);
        assertEq(agentBalance, SETTLEMENT_AMOUNT);
    }

    /**
     * @dev Test: Cannot release twice
     */
    function test_CannotReleaseTwice() public {
        vm.prank(employer);
        escrow.createSettlement(agent, SETTLEMENT_AMOUNT, "task-004");

        bytes32 settlementId = keccak256(abi.encodePacked(employer, agent, "task-004", block.timestamp));

        vm.prank(employer);
        escrow.releaseSettlement(settlementId);

        vm.prank(employer);
        vm.expectRevert("Already released");
        escrow.releaseSettlement(settlementId);
    }

    /**
     * @dev Test: Dispute settlement
     */
    function test_DisputeSettlement() public {
        vm.prank(employer);
        escrow.createSettlement(agent, SETTLEMENT_AMOUNT, "task-005");

        bytes32 settlementId = keccak256(abi.encodePacked(employer, agent, "task-005", block.timestamp));

        vm.prank(agent);
        escrow.disputeSettlement(settlementId);

        (, , , , bool isDisputed, ) = escrow.settlements(settlementId);
        assertTrue(isDisputed);
    }

    /**
     * @dev Test: Cannot release disputed settlement
     */
    function test_CannotReleaseDisputedSettlement() public {
        vm.prank(employer);
        escrow.createSettlement(agent, SETTLEMENT_AMOUNT, "task-006");

        bytes32 settlementId = keccak256(abi.encodePacked(employer, agent, "task-006", block.timestamp));

        vm.prank(agent);
        escrow.disputeSettlement(settlementId);

        vm.prank(employer);
        vm.expectRevert("Settlement is in dispute");
        escrow.releaseSettlement(settlementId);
    }

    /**
     * @dev Test: Resolve dispute - refund to employer
     */
    function test_ResolveDisputeRefundEmployer() public {
        vm.prank(employer);
        escrow.createSettlement(agent, SETTLEMENT_AMOUNT, "task-007");

        bytes32 settlementId = keccak256(abi.encodePacked(employer, agent, "task-007", block.timestamp));

        vm.prank(agent);
        escrow.disputeSettlement(settlementId);

        uint256 employerBalanceBefore = usdc.balanceOf(employer);

        vm.prank(owner);
        escrow.resolveDispute(settlementId, true);

        uint256 employerBalanceAfter = usdc.balanceOf(employer);
        assertEq(employerBalanceAfter - employerBalanceBefore, SETTLEMENT_AMOUNT);
    }

    /**
     * @dev Test: Resolve dispute - pay agent
     */
    function test_ResolveDisputePayAgent() public {
        vm.prank(employer);
        escrow.createSettlement(agent, SETTLEMENT_AMOUNT, "task-008");

        bytes32 settlementId = keccak256(abi.encodePacked(employer, agent, "task-008", block.timestamp));

        vm.prank(employer);
        escrow.disputeSettlement(settlementId);

        uint256 agentBalanceBefore = usdc.balanceOf(agent);

        vm.prank(owner);
        escrow.resolveDispute(settlementId, false);

        uint256 agentBalanceAfter = usdc.balanceOf(agent);
        assertEq(agentBalanceAfter - agentBalanceBefore, SETTLEMENT_AMOUNT);
    }

    /**
     * @dev Test: Agent reputation tracking
     */
    function test_AgentReputationTracking() public {
        vm.prank(employer);
        escrow.createSettlement(agent, SETTLEMENT_AMOUNT, "task-009");

        bytes32 settlementId = keccak256(abi.encodePacked(employer, agent, "task-009", block.timestamp));

        vm.prank(employer);
        escrow.releaseSettlement(settlementId);

        uint256 reputation = escrow.agentReputation(agent);
        assertEq(reputation, 1);
    }

    /**
     * @dev Test: Zero amount settlement should fail
     */
    function test_ZeroAmountFails() public {
        vm.prank(employer);
        vm.expectRevert("Amount must be greater than zero");
        escrow.createSettlement(agent, 0, "task-010");
    }

    /**
     * @dev Test: Insufficient balance fails
     */
    function test_InsufficientBalanceFails() public {
        address poorEmployer = address(0x4);
        usdc.mint(poorEmployer, 50 * 10 ** 6); // Only 50 USDC

        vm.prank(poorEmployer);
        usdc.approve(address(escrow), type(uint256).max);

        vm.prank(poorEmployer);
        vm.expectRevert();
        escrow.createSettlement(agent, SETTLEMENT_AMOUNT, "task-011");
    }

    /**
     * @dev Test: Unauthorized release fails
     */
    function test_UnauthorizedReleaseFails() public {
        vm.prank(employer);
        escrow.createSettlement(agent, SETTLEMENT_AMOUNT, "task-012");

        bytes32 settlementId = keccak256(abi.encodePacked(employer, agent, "task-012", block.timestamp));

        address unauthorized = address(0x5);
        vm.prank(unauthorized);
        vm.expectRevert("Not authorized");
        escrow.releaseSettlement(settlementId);
    }
}
