# Deployment & Testing Checklist

## Pre-Deployment Verification

### ✅ Smart Contract
- [ ] Solidity code reviewed
- [ ] Contract deploys without errors: `npm run compile` in blockchain/
- [ ] ABI generated: `npm run extract-abi`
- [ ] Constructor parameters set correctly

### ✅ Backend (Python)
- [ ] requirements.txt up to date
- [ ] All imports resolve correctly
- [ ] blockchain_client.py present in webapp/
- [ ] app_enhanced.py modified with new endpoints

### ✅ Frontend (React)
- [ ] LogViewer.jsx present
- [ ] Dashboard.jsx includes LogViewer import
- [ ] Build succeeds: `npm run build` in webapp/
- [ ] No TypeScript/JSX errors

---

## Deployment Steps

### Phase 1: Smart Contract Deployment

**Windows Powershell / CMD:**
```
1. Navigate to blockchain/
   cd blockchain

2. Install dependencies
   npm install

3. Compile the contract
   npm run compile

4. Start Hardhat node (Terminal 1)
   npm run node

5. Deploy contract (Terminal 2)
   npm run deploy:local

6. Extract ABI
   npm run extract-abi

7. Note the contract address
```

### Phase 2: Backend Configuration

**Create `webapp/.env`:**
```env
BLOCKCHAIN_CONTRACT_ADDRESS=0x...
BLOCKCHAIN_RPC_URL=http://127.0.0.1:8545
BLOCKCHAIN_PRIVATE_KEY=0x...
```

**Install Backend Dependencies:**
```bash
cd webapp
pip install -r requirements.txt
```

### Phase 3: Frontend Setup

**Install Frontend Dependencies:**
```bash
cd webapp
npm install --legacy-peer-deps
npm install @mui/lab --legacy-peer-deps
```

---

## Testing

### Test API Endpoints
```bash
# Get all logs
curl http://localhost:5000/api/logs?page=1&per_page=10

# Verify a log
curl http://localhost:5000/api/logs/0/verify
```

### Test Frontend
```bash
# Start dev server
cd webapp
npm run dev
# Open http://localhost:5173
# Login and navigate to Audit Logs
```

---

## Success Criteria

✅ All items must be checked:

- [ ] Smart contract deployed successfully
- [ ] Blockchain client connects without errors
- [ ] API endpoints respond correctly
- [ ] React UI renders without errors
- [ ] User registration logs events
- [ ] Authentication logs events
- [ ] LogViewer displays events
- [ ] Verification works correctly
- [ ] No console errors
- [ ] No Flask errors

---

**Status**: Ready for deployment ✅
