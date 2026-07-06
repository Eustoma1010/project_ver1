// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract VerdantTraceability {
    struct Milestone {
        string title;
        string description;
        string location;
        string actor;
        uint256 timestamp;
    }

    struct BatchInfo {
        string batchId;
        string productName;
        string farmName;
        bool exists;
        Milestone[] milestones;
        bytes32[] deliveryHashes;
    }

    mapping(string => BatchInfo) private batches;

    event BatchRegistered(string indexed batchId, string productName, string farmName, uint256 timestamp);
    event MilestoneAdded(string indexed batchId, string title, string location, uint256 timestamp);
    event DeliveryRecorded(string indexed batchId, bytes32 indexed deliveryHash, uint256 timestamp);

    function registerBatch(
        string memory _batchId,
        string memory _productName,
        string memory _farmName
    ) public {
        require(!batches[_batchId].exists, "Batch ID already exists");

        BatchInfo storage newBatch = batches[_batchId];
        newBatch.batchId = _batchId;
        newBatch.productName = _productName;
        newBatch.farmName = _farmName;
        newBatch.exists = true;

        emit BatchRegistered(_batchId, _productName, _farmName, block.timestamp);
    }

    function addMilestone(
        string memory _batchId,
        string memory _title,
        string memory _description,
        string memory _location,
        string memory _actor
    ) public {
        require(batches[_batchId].exists, "Batch does not exist");

        batches[_batchId].milestones.push(Milestone({
            title: _title,
            description: _description,
            location: _location,
            actor: _actor,
            timestamp: block.timestamp
        }));

        emit MilestoneAdded(_batchId, _title, _location, block.timestamp);
    }

    function recordDelivery(string memory _batchId, bytes32 _deliveryHash) public {
        require(batches[_batchId].exists, "Batch does not exist");
        
        batches[_batchId].deliveryHashes.push(_deliveryHash);

        emit DeliveryRecorded(_batchId, _deliveryHash, block.timestamp);
    }

    function getBatchJourney(string memory _batchId) public view returns (
        string memory batchId,
        string memory productName,
        string memory farmName,
        Milestone[] memory milestones,
        bytes32[] memory deliveryHashes
    ) {
        require(batches[_batchId].exists, "Batch does not exist");
        BatchInfo storage b = batches[_batchId];
        return (b.batchId, b.productName, b.farmName, b.milestones, b.deliveryHashes);
    }
}
