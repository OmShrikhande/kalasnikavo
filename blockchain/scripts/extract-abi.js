const fs = require("fs");
const path = require("path");

const artifactPath = path.join(__dirname, "..", "artifacts", "contracts", "BiometricAuditLog.sol", "BiometricAuditLog.json");

if (!fs.existsSync(artifactPath)) {
  console.error("Error: BiometricAuditLog.json artifact not found.");
  console.error("Please run: npm run compile");
  process.exit(1);
}

const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf8"));
const abi = artifact.abi;

const outputPath = path.join(__dirname, "..", "BiometricAuditLog_abi.json");
fs.writeFileSync(outputPath, JSON.stringify(abi, null, 2));

console.log(`✅ ABI extracted to: ${outputPath}`);
