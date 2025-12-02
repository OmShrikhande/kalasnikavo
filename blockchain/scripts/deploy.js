const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  console.log("Deploying BiometricAuditLog contract...");

  const BiometricAuditLog = await hre.ethers.getContractFactory("BiometricAuditLog");
  const contract = await BiometricAuditLog.deploy();

  await contract.waitForDeployment();

  const contractAddress = await contract.getAddress();
  console.log("BiometricAuditLog deployed to:", contractAddress);

  const abi = BiometricAuditLog.interface.formatJson();
  
  const abiPath = path.join(__dirname, "..", "BiometricAuditLog_abi.json");
  fs.writeFileSync(abiPath, JSON.stringify(JSON.parse(abi), null, 2));
  console.log("ABI saved to:", abiPath);

  const envContent = `BLOCKCHAIN_CONTRACT_ADDRESS=${contractAddress}
BLOCKCHAIN_RPC_URL=http://127.0.0.1:8545
BLOCKCHAIN_PRIVATE_KEY=${(await hre.ethers.getSigners())[0].privateKey}
`;

  const envPath = path.join(__dirname, "..", ".env.blockchain");
  fs.writeFileSync(envPath, envContent);
  console.log("Environment variables saved to:", envPath);

  console.log("\n✅ Deployment completed successfully!");
  console.log("Next steps:");
  console.log("1. Copy the contract address and update your .env file");
  console.log("2. Copy the private key from .env.blockchain to your main .env");
  console.log("3. Update BLOCKCHAIN_CONTRACT_ADDRESS and BLOCKCHAIN_PRIVATE_KEY in your Flask .env");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
