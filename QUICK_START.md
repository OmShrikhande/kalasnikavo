# Quick Start Guide - Blockchain Audit Logging Integration

## 🚀 Get Up and Running in 5 Steps

### Step 1: Install Blockchain Dependencies (if not already done)
```bash
cd blockchain
npm install
npm run compile
```

### Step 2: Deploy Smart Contract
```bash
# For local testing (requires Hardhat node running)
npm run node  # In terminal 1
npm run deploy:local  # In terminal 2

# For Sepolia testnet
npm run deploy:sepolia
```

### Step 3: Configure Environment
Copy the contract address and create `webapp/.env`:
```env
BLOCKCHAIN_CONTRACT_ADDRESS=0x...  (from deploy output)
BLOCKCHAIN_RPC_URL=http://127.0.0.1:8545
BLOCKCHAIN_PRIVATE_KEY=0x...  (from deploy output)
```

### Step 4: Install and Run Backend
```bash
cd webapp
pip install -r requirements.txt
python app_enhanced.py
```

### Step 5: Install and Run Frontend
```bash
cd webapp
npm install --legacy-peer-deps
npm install @mui/lab
npm run dev
```

---

## 📋 File Locations

| Component | File | Status |
|-----------|------|--------|
| Smart Contract | `blockchain/contracts/BiometricAuditLog.sol` | ✅ Created |
| Deploy Script | `blockchain/scripts/deploy.js` | ✅ Created |
| Blockchain Client | `webapp/blockchain_client.py` | ✅ Enhanced |
| API Endpoints | `webapp/app_enhanced.py` | ✅ Modified |
| LogViewer UI | `webapp/src/LogViewer.jsx` | ✅ Created |
| Dashboard Integration | `webapp/src/Dashboard.jsx` | ✅ Modified |

---

## 🔑 Key Commands

```bash
# Blockchain
cd blockchain
npm run compile           # Compile contract
npm run deploy:local      # Deploy to local Hardhat node
npm run deploy:sepolia    # Deploy to Sepolia testnet
npm run extract-abi       # Extract contract ABI

# Backend
cd webapp
python app_enhanced.py    # Start Flask server

# Frontend
cd webapp
npm run dev               # Start Vite dev server
npm run build             # Build for production
```

---

## 🔗 API Endpoints

### Get All Logs
```bash
GET /api/logs?page=1&per_page=50
```

### Verify Log Integrity
```bash
GET /api/logs/0/verify
```

### Register User (Auto-logs ENROLL event)
```bash
POST /api/register
```

### Face Authentication (Auto-logs AUTH_SUCCESS or AUTH_FAIL)
```bash
POST /api/auth/face
```

### Fingerprint Authentication (Auto-logs AUTH_SUCCESS or AUTH_FAIL)
```bash
POST /api/auth/fingerprint
```

---

## 👁️ View Logs

1. Login to the application
2. Click **"Audit Logs"** button in Dashboard
3. Choose view mode:
   - **Table View**: Compact table of all logs
   - **Timeline View**: Visual timeline
4. Click **"Verify"** on any log to check integrity

---

## ⚠️ Important Notes

1. **Blockchain Network**: Ensure you have a running Hardhat node OR configure Sepolia RPC
2. **Private Key**: Keep `BLOCKCHAIN_PRIVATE_KEY` secure - it has real gas costs on testnet
3. **Contract Address**: After deployment, update `.env` with the contract address
4. **Python Version**: Requires Python 3.8+
5. **Node Version**: Requires Node.js 16+ for Hardhat

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ABI file not found` | Run `npm run compile && npm run extract-abi` in blockchain/ |
| `Cannot connect to blockchain` | Verify RPC_URL and ensure network is running |
| `@mui/lab not found` | Run `npm install @mui/lab --legacy-peer-deps` |
| `Failed to build React` | Run `npm install --legacy-peer-deps` first |

---

## 📚 Documentation

- Full integration guide: `INTEGRATION_COMPLETE.md`
- Smart contract details: `blockchain/contracts/BiometricAuditLog.sol`
- Python blockchain client: `webapp/blockchain_client.py`
- Flask API routes: `webapp/app_enhanced.py` (lines 1598-1689)
- React component: `webapp/src/LogViewer.jsx`

---

## ✅ What's Implemented

- ✅ Immutable blockchain audit logs
- ✅ Privacy-preserving hash-based storage
- ✅ Automatic logging on enrollment and authentication
- ✅ Beautiful React UI for viewing logs
- ✅ Log integrity verification
- ✅ Timeline and table view modes
- ✅ Pagination support
- ✅ Full error handling

---

## 🔐 Security Features

- ✅ Biometric data never stored on-chain
- ✅ Personal identifiers never stored on-chain
- ✅ SHA-256 hashing for sensitive fields
- ✅ Immutable audit trail
- ✅ Off-chain metadata storage
- ✅ Event-based indexing
- ✅ Rate limiting on API endpoints

---

**Ready to test? Start with Step 1 above!** 🎉
