const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("VerdantTraceability", function () {
  it("Should perform full batch journey lifecycle correctly", async function () {
    const Contract = await ethers.getContractFactory("VerdantTraceability");
    const contract = await Contract.deploy();
    await contract.waitForDeployment();

    // 1. Register Batch
    await contract.registerBatch("BATCH-01", "Cải xoăn kale", "Nông trại Mùa");
    
    // 2. Add Milestones
    await contract.addMilestone("BATCH-01", "Gieo hạt", "Xuống giống hạt cải xoăn hữu cơ", "Đà Lạt", "Nông dân Mùa");
    await contract.addMilestone("BATCH-01", "Bón phân", "Bón phân hữu cơ sinh học đợt 1", "Đà Lạt", "Nông dân Mùa");
    await contract.addMilestone("BATCH-01", "Thu hoạch", "Thu hoạch cải xoăn tươi đóng gói", "Đà Lạt", "Nông dân Mùa");

    // 3. Record Delivery Hash (SHA-256 / Keccak-256)
    const deliveryHash = ethers.solidityPackedKeccak256(
      ["string", "string", "string"],
      ["ORDER-1001", "Nguyễn Văn A", "Quận 1, TP. Hồ Chí Minh"]
    );
    await contract.recordDelivery("BATCH-01", deliveryHash);

    // 4. Retrieve Journey
    const journey = await contract.getBatchJourney("BATCH-01");

    expect(journey.batchId).to.equal("BATCH-01");
    expect(journey.productName).to.equal("Cải xoăn kale");
    expect(journey.farmName).to.equal("Nông trại Mùa");
    expect(journey.milestones.length).to.equal(3);
    expect(journey.milestones[0].title).to.equal("Gieo hạt");
    expect(journey.deliveryHashes.length).to.equal(1);
    expect(journey.deliveryHashes[0]).to.equal(deliveryHash);
  });
});
