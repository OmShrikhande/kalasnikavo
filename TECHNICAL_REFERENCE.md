# Technical Reference - Blockchain Audit Logging

## Table of Contents
1. [Smart Contract API](#smart-contract-api)
2. [Python Blockchain Client API](#python-blockchain-client-api)
3. [Flask API Endpoints](#flask-api-endpoints)
4. [React Component API](#react-component-api)
5. [Data Models](#data-models)
6. [Event Types](#event-types)
7. [Error Handling](#error-handling)

---

## Smart Contract API

### Contract: `BiometricAuditLog`
**Location**: `blockchain/contracts/BiometricAuditLog.sol`
**Solidity Version**: ^0.8.20
**License**: MIT

### Data Structures

#### LogEntry Struct
```solidity
struct LogEntry {
    bytes32 userIdHash;    // SHA-256 hash of user internal ID
    EventType eventType;   // 0=ENROLL, 1=AUTH_SUCCESS, 2=AUTH_FAIL, 3=ADMIN_ACTION
    uint64 timestamp;      // Unix timestamp (seconds)
    bytes32 metaHash;      // SHA-256 hash of JSON metadata
}
```

#### EventType Enum
```solidity
enum EventType { 
    ENROLL,        // 0
    AUTH_SUCCESS,  // 1
    AUTH_FAIL,     // 2
    ADMIN_ACTION   // 3
}
```

### Functions

#### `addLog(bytes32 userIdHash, EventType eventType, uint64 timestamp, bytes32 metaHash)`
**Type**: External, State-Changing
**Gas**: ~21,000 (write to storage)
**Access**: Public (anyone can call)

Adds a new log entry to the chain.

**Parameters:**
- `userIdHash`: bytes32 - SHA-256 hash of user's internal ID
- `eventType`: EventType - Type of event (0-3)
- `timestamp`: uint64 - Unix timestamp
- `metaHash`: bytes32 - SHA-256 hash of metadata JSON

**Emits**: `LogRecorded(logIndex, userIdHash, eventType, timestamp, metaHash)`

**Returns**: None

**Example:**
```solidity
bytes32 userHash = 0x...;
contract.addLog(userHash, 0, 1701512400, metaHash);
```

#### `getLog(uint256 index) → (bytes32, EventType, uint64, bytes32)`
**Type**: External, View
**Gas**: ~3,000 (read from storage)

Retrieves a specific log entry.

**Parameters:**
- `index`: uint256 - Log entry index (0-based)

**Returns:**
- bytes32: userIdHash
- EventType: Event type (0-3)
- uint64: Timestamp
- bytes32: metaHash

**Reverts**: If index >= logs.length

**Example:**
```solidity
(bytes32 userHash, uint eventType, uint64 time, bytes32 metaHash) = contract.getLog(0);
```

#### `totalLogs() → uint256`
**Type**: External, View
**Gas**: ~2,600 (read from storage)

Returns total number of logged entries.

**Parameters**: None

**Returns**: uint256 - Total log count

**Example:**
```solidity
uint256 total = contract.totalLogs();
```

### Events

#### `LogRecorded(uint256 indexed logIndex, bytes32 indexed userIdHash, EventType eventType, uint64 timestamp, bytes32 metaHash)`

Emitted when a log entry is added.

**Indexed Parameters:**
- `logIndex`: Position in the logs array
- `userIdHash`: Hash of user ID (allows filtering by user)

**Non-Indexed:**
- `eventType`: Type of event
- `timestamp`: When it occurred
- `metaHash`: Hash of metadata

**Use for Querying:**
```javascript
// Get all logs for a specific user
const events = await contract.queryFilter('LogRecorded', 0, 'latest', {
  userIdHash: userHash
});
```

---

## Python Blockchain Client API

### Module: `webapp/blockchain_client.py`

### Configuration

**Environment Variables:**
```python
BLOCKCHAIN_RPC_URL = "http://127.0.0.1:8545"  # Default RPC endpoint
BLOCKCHAIN_PRIVATE_KEY = "0x..."              # Account private key
BLOCKCHAIN_CONTRACT_ADDRESS = "0x..."         # Deployed contract address
```

### Classes & Functions

#### `log_biometric_event()`

```python
def log_biometric_event(
    user_internal_id: str,
    event_type: str,
    meta_obj: dict,
    timestamp: Optional[int] = None,
) -> Optional[Dict]:
```

**Purpose**: Log a biometric event to the blockchain.

**Parameters:**
- `user_internal_id` (str): Internal user ID (will be hashed)
- `event_type` (str): One of ['ENROLL', 'AUTH_SUCCESS', 'AUTH_FAIL', 'ADMIN_ACTION']
- `meta_obj` (dict): Metadata dictionary (stored off-chain, hashed on-chain)
- `timestamp` (Optional[int]): Unix timestamp (default: current time)

**Returns:**
```python
{
    'tx_hash': '0x...',      # Transaction hash
    'log_index': 0,          # Index of log entry
    'timestamp': 1701512400  # Unix timestamp
}
```

**Raises**: ValueError if event_type is invalid

**Side Effects**: 
- Sends transaction to blockchain
- Stores metadata locally
- Waits for receipt (30 second timeout)

**Example:**
```python
result = log_biometric_event(
    user_internal_id="user_123",
    event_type="ENROLL",
    meta_obj={
        "email": "user@example.com",
        "security_level": "MEDIUM"
    }
)
# Returns: {'tx_hash': '0x...', 'log_index': 0, 'timestamp': 1701512400}
```

#### `get_all_logs()`

```python
def get_all_logs() -> List[Dict]:
```

**Purpose**: Fetch all logs from the blockchain.

**Parameters**: None

**Returns:**
```python
[
    {
        'index': 0,
        'userIdHash': '0x...',
        'eventType': 'ENROLL',
        'timestamp': 1701512400,
        'metaHash': '0x...'
    },
    # ... more entries
]
```

**Example:**
```python
logs = get_all_logs()
for log in logs:
    print(f"Log {log['index']}: {log['eventType']}")
```

#### `get_log()`

```python
def get_log(index: int) -> Optional[Dict]:
```

**Purpose**: Fetch a specific log by index.

**Parameters:**
- `index` (int): Log entry index

**Returns:**
```python
{
    'index': 0,
    'userIdHash': '0x...',
    'eventType': 'ENROLL',
    'timestamp': 1701512400,
    'metaHash': '0x...'
}
```

**Returns None**: If index out of range or error occurs

**Example:**
```python
log = get_log(0)
if log:
    print(log['eventType'])
```

#### `verify_metadata()`

```python
def verify_metadata(meta_obj: dict, on_chain_meta_hash: str) -> bool:
```

**Purpose**: Verify that metadata matches the on-chain hash.

**Parameters:**
- `meta_obj` (dict): Metadata dictionary to verify
- `on_chain_meta_hash` (str): Hash from blockchain (with or without 0x prefix)

**Returns:**
- bool: True if hashes match, False otherwise

**Process:**
1. Converts meta_obj to canonical JSON
2. Computes SHA-256 hash
3. Compares with on_chain_meta_hash

**Example:**
```python
metadata = {"email": "user@example.com"}
is_valid = verify_metadata(metadata, "0xabcd1234...")
```

#### `store_metadata()`

```python
def store_metadata(user_id: str, log_index: int, metadata: dict) -> None:
```

**Purpose**: Store metadata off-chain (in-memory).

**Parameters:**
- `user_id` (str): User ID
- `log_index` (int): Log entry index
- `metadata` (dict): Metadata to store

**Storage**: In-memory dictionary (note: lost on restart)

**Example:**
```python
store_metadata("user_123", 0, {"email": "user@example.com"})
```

#### `retrieve_metadata()`

```python
def retrieve_metadata(user_id: str, log_index: int) -> Optional[dict]:
```

**Purpose**: Retrieve stored metadata off-chain.

**Parameters:**
- `user_id` (str): User ID
- `log_index` (int): Log entry index

**Returns:** Metadata dict or None if not found

**Example:**
```python
metadata = retrieve_metadata("user_123", 0)
```

#### `get_total_logs()`

```python
def get_total_logs() -> int:
```

**Purpose**: Get total number of logs on blockchain.

**Parameters**: None

**Returns:** Total count (int)

**Example:**
```python
total = get_total_logs()
print(f"Total logs: {total}")
```

### Helper Functions

#### `sha256_hex()`
```python
def sha256_hex(data: str) -> str:
```
Returns SHA-256 hash as hex string.

#### `canonical_json()`
```python
def canonical_json(obj: dict) -> str:
```
Converts dict to canonical JSON (sorted keys, no spaces).

#### `to_bytes32()`
```python
def to_bytes32(hex_str: str) -> bytes:
```
Converts hex string to bytes32 (padded/truncated to 64 hex chars).

---

## Flask API Endpoints

### Base URL: `http://localhost:5000`

### Endpoint: GET `/api/logs`

**Purpose**: Fetch paginated blockchain logs

**Query Parameters:**
- `page` (int, default: 1): Page number (1-based)
- `per_page` (int, default: 50): Logs per page (max: 100)

**Response (200 OK):**
```json
{
  "success": true,
  "logs": [
    {
      "index": 0,
      "userIdHash": "0xabcd1234...",
      "eventType": "ENROLL",
      "timestamp": 1701512400,
      "metaHash": "0xef567890..."
    }
  ],
  "total": 150,
  "page": 1,
  "per_page": 50,
  "pages": 3
}
```

**Error Response (500):**
```json
{
  "error": "Failed to fetch logs"
}
```

**Example:**
```bash
curl "http://localhost:5000/api/logs?page=1&per_page=10"
```

### Endpoint: GET `/api/logs/<log_index>/verify`

**Purpose**: Verify a log entry's integrity

**Path Parameters:**
- `log_index` (int): Log entry index

**Response (200 OK - Verified):**
```json
{
  "success": true,
  "verified": true,
  "log_index": 0,
  "log_entry": {
    "index": 0,
    "userIdHash": "0xabcd1234...",
    "eventType": "ENROLL",
    "timestamp": 1701512400,
    "metaHash": "0xef567890..."
  },
  "stored_metadata": {
    "email": "user@example.com",
    "security_level": "MEDIUM"
  },
  "message": "Metadata integrity verified"
}
```

**Response (200 OK - Not Verified):**
```json
{
  "success": true,
  "verified": false,
  "log_entry": {...},
  "stored_metadata": {...},
  "message": "Metadata integrity check failed"
}
```

**Response (200 OK - No Metadata):**
```json
{
  "success": true,
  "verified": false,
  "reason": "Metadata not available for verification (off-chain storage)",
  "log_entry": {...}
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "Log entry not found"
}
```

**Error Response (500):**
```json
{
  "error": "Failed to verify log",
  "details": "error details here"
}
```

**Example:**
```bash
curl "http://localhost:5000/api/logs/0/verify"
```

---

## React Component API

### Component: `LogViewer`

**Location**: `webapp/src/LogViewer.jsx`

**Props**: None (uses internal state and API calls)

**State:**
```javascript
{
  logs: [],                    // Array of log objects
  loading: boolean,            // Loading state
  error: string | null,        // Error message
  page: number,               // Current page (1-based)
  perPage: number,            // Logs per page
  totalPages: number,         // Total pages
  viewMode: number,           // 0=Table, 1=Timeline
  selectedLog: object | null, // Selected log for verification
  verificationDialog: boolean, // Show verification dialog
  verificationResult: object | null, // Verification result
  verifying: boolean,         // Verification in progress
  copied: boolean,            // Clipboard copy success
  copiedField: string | null  // Which field was copied
}
```

**Hooks Used:**
- `useState`: State management
- `useEffect`: Data fetching on mount/page change

**Functions:**

#### `fetchLogs()`
Fetches logs from `/api/logs` endpoint.

#### `handleVerify(logIndex)`
Verifies a specific log by calling `/api/logs/<logIndex>/verify`.

#### `handleCopyToClipboard(text, field)`
Copies text to clipboard and shows feedback.

#### `getEventIcon(eventType)`
Returns Material-UI icon for event type.

#### `getEventColor(eventType)`
Returns color string for event type.

#### `formatTimestamp(timestamp)`
Formats Unix timestamp to readable date string.

#### `formatHash(hash)`
Truncates hash to first 10 + last 8 characters.

#### `truncateHash(hash, length)`
Truncates hash to specified length.

**View Modes:**

**Table View:**
- Columns: Event Type, User ID Hash, Timestamp, Metadata Hash, Actions
- Shows copy button for hashes
- Verify button for each row

**Timeline View:**
- Vertical timeline with cards
- Color-coded event types
- Expandable details
- Verify button on each card

**Features:**
- ✅ Pagination (1-based)
- ✅ Copy-to-clipboard with visual feedback
- ✅ Integrity verification dialog
- ✅ Dual view modes (Table/Timeline)
- ✅ Manual refresh button
- ✅ Error handling and loading states
- ✅ Material-UI components and animations

---

## Data Models

### Log Entry Model

**On-Chain (Smart Contract):**
```python
{
    "index": int,              # Array index
    "userIdHash": str,         # 0x-prefixed hex (32 bytes)
    "eventType": int,          # 0-3
    "timestamp": int,          # Unix seconds
    "metaHash": str            # 0x-prefixed hex (32 bytes)
}
```

**Off-Chain (Database/Local):**
```python
{
    "user_id": str,            # Internal user ID
    "log_index": int,          # Reference to on-chain log
    "metadata": dict,          # Full metadata object
    "stored_at": int           # Unix timestamp when stored
}
```

### Metadata Model

**Structure:**
```json
{
  "email": "user@example.com",
  "security_level": "MEDIUM",
  "face_quality": 0.92,
  "fingerprint_quality": 0.88,
  "registration_time": 2.34,
  "device_fingerprint": "...",
  "registration_location": "...",
  "confidence": 95.5,
  "ip_address": "192.168.1.1",
  "location": "New York, USA",
  "response_time": 1.23
}
```

---

## Event Types

### Enum Values

| Name | Value | Description |
|------|-------|-------------|
| ENROLL | 0 | User registration/enrollment |
| AUTH_SUCCESS | 1 | Successful authentication |
| AUTH_FAIL | 2 | Failed authentication attempt |
| ADMIN_ACTION | 3 | Administrative action |

### Event Metadata by Type

**ENROLL (0):**
```json
{
  "email": "...",
  "security_level": "MEDIUM",
  "face_quality": 0.92,
  "fingerprint_quality": 0.88,
  "registration_time": 2.34,
  "device_fingerprint": "...",
  "registration_location": "..."
}
```

**AUTH_SUCCESS (1):**
```json
{
  "confidence": 95.5,
  "response_time": 1.23,
  "quality": 0.89,
  "device_fingerprint": "...",
  "ip_address": "192.168.1.1",
  "location": "New York, USA"
}
```

**AUTH_FAIL (2):**
```json
{
  "confidence": 65.3,
  "required": 80.0,
  "response_time": 1.23,
  "device_fingerprint": "...",
  "ip_address": "192.168.1.1",
  "location": "New York, USA"
}
```

**ADMIN_ACTION (3):**
```json
{
  "action": "reset_password",
  "admin_id": "admin_456",
  "target_user": "user_123",
  "timestamp": 1701512400,
  "reason": "User requested reset"
}
```

---

## Error Handling

### Python Exceptions

**ValueError:**
- Raised when invalid event_type is provided
- Example: `ValueError("Invalid event_type: UNKNOWN")`

**Exception:**
- Generic exception wrapper for blockchain operations
- Logged but not raised (returns None instead)

### HTTP Status Codes

| Code | Endpoint | Meaning |
|------|----------|---------|
| 200 | All | Success |
| 400 | All | Bad request / Invalid parameters |
| 404 | /verify | Log entry not found |
| 500 | All | Server error |

### Error Response Format

```json
{
  "error": "Error message",
  "details": "Additional details (if available)"
}
```

### Logging

All errors are logged using Python's `logging` module:
```python
logger.error(f"Error message: {e}")
```

---

## Testing Examples

### Python Testing

```python
from blockchain_client import log_biometric_event, get_all_logs

# Log an event
result = log_biometric_event("user_123", "ENROLL", {"email": "test@example.com"})
print(result)  # {'tx_hash': '0x...', 'log_index': 0, 'timestamp': 1701512400}

# Get all logs
logs = get_all_logs()
print(f"Total logs: {len(logs)}")

# Verify log
is_valid = verify_metadata({"email": "test@example.com"}, result['metaHash'])
print(f"Verified: {is_valid}")
```

### JavaScript/React Testing

```javascript
// Fetch logs
const response = await fetch('/api/logs?page=1&per_page=10');
const data = await response.json();
console.log(data.logs);

// Verify specific log
const verifyResponse = await fetch('/api/logs/0/verify');
const verifyData = await verifyResponse.json();
console.log(verifyData.verified);
```

### cURL Testing

```bash
# Get all logs
curl http://localhost:5000/api/logs?page=1&per_page=5

# Verify specific log
curl http://localhost:5000/api/logs/0/verify

# Pretty print JSON
curl http://localhost:5000/api/logs | python -m json.tool
```

---

## Performance Metrics

### Gas Usage (Approx.)
- `addLog()`: ~21,000 gas
- `getLog()`: ~3,000 gas (read-only)
- `totalLogs()`: ~2,600 gas (read-only)

### Latency (Typical)
- Local Hardhat: 1-2 seconds per transaction
- Sepolia testnet: 15-30 seconds per transaction
- Mainnet: 20+ seconds (varies by congestion)

### Storage
- Per log on-chain: ~96 bytes
- Per metadata off-chain: ~200-500 bytes
- Blockchain bloat: Minimal (only hashes)

---

## Security Considerations

1. **Private Key Management**: Never commit PRIVATE_KEY to version control
2. **Rate Limiting**: API endpoints have rate limiting (10-100 requests/minute)
3. **Gas Price**: Monitor gas prices before production deployment
4. **Data Validation**: All inputs are validated before blockchain operations
5. **Hash Collisions**: SHA-256 provides negligible collision risk (2^256)
6. **Immutability**: Once logged, data cannot be modified or deleted

---

**End of Technical Reference**
