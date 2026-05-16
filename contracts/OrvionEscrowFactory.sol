// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./OrvionEscrow.sol";

/**
 * @title OrvionEscrowFactory
 * @dev Permite a criação de múltiplas instâncias de Settlement Layers para diferentes projetos.
 */
contract OrvionEscrowFactory {
    address[] public allEscrows;
    mapping(address => address[]) public creatorEscrows;

    event EscrowCreated(address indexed creator, address escrowAddress, address usdcToken);

    /**
     * @dev Cria um novo contrato de Escrow para um projeto específico.
     */
    function createEscrow(address _usdcToken) external returns (address) {
        OrvionEscrow newEscrow = new OrvionEscrow(_usdcToken);
        newEscrow.transferOwnership(msg.sender);
        
        address escrowAddr = address(newEscrow);
        allEscrows.push(escrowAddr);
        creatorEscrows[msg.sender].push(escrowAddr);

        emit EscrowCreated(msg.sender, escrowAddr, _usdcToken);
        return escrowAddr;
    }

    function getEscrowCount() external view returns (uint256) {
        return allEscrows.length;
    }

    function getEscrowsByCreator(address _creator) external view returns (address[] memory) {
        return creatorEscrows[_creator];
    }
}
