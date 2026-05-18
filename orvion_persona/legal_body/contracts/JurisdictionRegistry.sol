// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title JurisdictionRegistry
 * @notice On-chain index of supported legal jurisdictions and the
 *         statutory citations that authorize agent-controlled entities.
 *         Used by AgentPersona.sol and front-end wizards to validate
 *         incorporation requests.
 */
contract JurisdictionRegistry {
    struct Jurisdiction {
        string  name;             // e.g. "Wyoming DAO LLC"
        string  isoCode;          // e.g. "US-WY"
        string  statuteCitation;  // e.g. "W.S. 17-31-101"
        string  templateURI;      // ipfs://... base Operating Agreement template
        bool    supportsZeroMember;
        bool    active;
    }

    mapping(uint8 => Jurisdiction) public jurisdictions;
    address public governance;

    event JurisdictionAdded(uint8 indexed id, string name);
    event JurisdictionUpdated(uint8 indexed id);

    constructor() {
        governance = msg.sender;

        jurisdictions[0] = Jurisdiction({
            name: "Wyoming DAO LLC",
            isoCode: "US-WY",
            statuteCitation: "W.S. 17-31-101 et seq.",
            templateURI: "ipfs://orvion-templates/wyoming-dao-llc.yaml",
            supportsZeroMember: true,
            active: true
        });

        jurisdictions[1] = Jurisdiction({
            name: "Delaware Series LLC",
            isoCode: "US-DE",
            statuteCitation: "6 Del. C. § 18-215",
            templateURI: "ipfs://orvion-templates/delaware-series-llc.yaml",
            supportsZeroMember: false,
            active: true
        });

        jurisdictions[2] = Jurisdiction({
            name: "New York LLC",
            isoCode: "US-NY",
            statuteCitation: "N.Y. LLC Law § 203",
            templateURI: "ipfs://orvion-templates/new-york-llc.yaml",
            supportsZeroMember: false,
            active: true
        });

        jurisdictions[3] = Jurisdiction({
            name: "Marshall Islands DAO",
            isoCode: "MH",
            statuteCitation: "Marshall Islands Non-Profit Entities Act 2021",
            templateURI: "ipfs://orvion-templates/marshall-islands-dao.yaml",
            supportsZeroMember: true,
            active: true
        });
    }

    modifier onlyGov() {
        require(msg.sender == governance, "JR: not gov");
        _;
    }

    function addJurisdiction(uint8 id, Jurisdiction calldata j) external onlyGov {
        jurisdictions[id] = j;
        emit JurisdictionAdded(id, j.name);
    }

    function setActive(uint8 id, bool active) external onlyGov {
        jurisdictions[id].active = active;
        emit JurisdictionUpdated(id);
    }
}
