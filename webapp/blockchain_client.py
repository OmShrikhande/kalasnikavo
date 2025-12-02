import json
import time
import hashlib
import logging
import os
from pathlib import Path
from typing import Dict, Optional, Tuple, List
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

RPC_URL = os.getenv("BLOCKCHAIN_RPC_URL", "http://127.0.0.1:8545")
PRIVATE_KEY = os.getenv("BLOCKCHAIN_PRIVATE_KEY")
CONTRACT_ADDRESS_STR = os.getenv("BLOCKCHAIN_CONTRACT_ADDRESS", "0x0000000000000000000000000000000000000000")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

try:
    ABI_PATH = Path(__file__).parent / "BiometricAuditLog_abi.json"
    if ABI_PATH.exists():
        with ABI_PATH.open() as f:
            CONTRACT_ABI = json.load(f)
    else:
        CONTRACT_ABI = []
        logger.warning(f"ABI file not found at {ABI_PATH}")
except Exception as e:
    logger.error(f"Failed to load ABI: {e}")
    CONTRACT_ABI = []

try:
    CONTRACT_ADDRESS = Web3.to_checksum_address(CONTRACT_ADDRESS_STR)
    if CONTRACT_ABI:
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    else:
        contract = None
except Exception as e:
    logger.warning(f"Failed to initialize contract: {e}")
    contract = None

SENDER_ADDRESS = None
if PRIVATE_KEY:
    try:
        account = w3.eth.account.from_key(PRIVATE_KEY)
        SENDER_ADDRESS = account.address
    except Exception as e:
        logger.warning(f"Failed to initialize account from private key: {e}")


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def to_bytes32(hex_str: str) -> bytes:
    if hex_str.startswith("0x"):
        hex_str = hex_str[2:]
    hex_str = hex_str.ljust(64, "0")[:64]
    return bytes.fromhex(hex_str)


def canonical_json(obj: dict) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def log_biometric_event(
    user_internal_id: str,
    event_type: str,
    meta_obj: dict,
    timestamp: Optional[int] = None,
) -> Optional[Dict]:
    """
    Log a biometric event to the blockchain.
    
    Args:
        user_internal_id: Internal user ID (will be hashed)
        event_type: One of ['ENROLL', 'AUTH_SUCCESS', 'AUTH_FAIL', 'ADMIN_ACTION']
        meta_obj: Metadata dictionary (will be stored off-chain, hashed on-chain)
        timestamp: Unix timestamp (default: current time)
    
    Returns:
        Dictionary with tx_hash and log_index, or None if failed
    """
    if not contract or not SENDER_ADDRESS:
        logger.warning("Blockchain not configured. Skipping blockchain logging.")
        return None

    event_type_map = {
        "ENROLL": 0,
        "AUTH_SUCCESS": 1,
        "AUTH_FAIL": 2,
        "ADMIN_ACTION": 3,
    }

    if event_type not in event_type_map:
        raise ValueError(f"Invalid event_type: {event_type}")

    if timestamp is None:
        timestamp = int(time.time())

    user_id_hash_hex = sha256_hex(user_internal_id)
    user_id_hash_bytes32 = to_bytes32(user_id_hash_hex)

    meta_json = canonical_json(meta_obj)
    meta_hash_hex = sha256_hex(meta_json)
    meta_hash_bytes32 = to_bytes32(meta_hash_hex)

    try:
        nonce = w3.eth.get_transaction_count(SENDER_ADDRESS)

        tx = contract.functions.addLog(
            user_id_hash_bytes32,
            event_type_map[event_type],
            timestamp,
            meta_hash_bytes32,
        ).build_transaction(
            {
                "from": SENDER_ADDRESS,
                "nonce": nonce,
                "gas": 300000,
                "maxFeePerGas": w3.to_wei("2", "gwei"),
                "maxPriorityFeePerGas": w3.to_wei("1", "gwei"),
            }
        )

        if PRIVATE_KEY:
            signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        else:
            tx_hash = w3.eth.send_transaction(tx)

        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
        
        log_index = len(get_all_logs()) - 1 if get_all_logs() else 0

        logger.info(f"Logged event {event_type} for user {user_id_hash_hex[:8]}... tx={tx_hash.hex()}")
        
        return {
            "tx_hash": tx_hash.hex(),
            "log_index": log_index,
            "timestamp": timestamp,
        }

    except Exception as e:
        logger.error(f"Failed to log blockchain event: {e}")
        return None


def get_all_logs() -> List[Dict]:
    """Fetch all logs from blockchain."""
    if not contract:
        return []

    try:
        total = contract.functions.totalLogs().call()
        logs = []
        for i in range(total):
            user_id_hash, event_type_num, timestamp, meta_hash = contract.functions.getLog(i).call()
            event_types = ["ENROLL", "AUTH_SUCCESS", "AUTH_FAIL", "ADMIN_ACTION"]
            logs.append({
                "index": i,
                "userIdHash": user_id_hash.hex(),
                "eventType": event_types[event_type_num] if event_type_num < len(event_types) else "UNKNOWN",
                "timestamp": timestamp,
                "metaHash": meta_hash.hex(),
            })
        return logs
    except Exception as e:
        logger.error(f"Failed to fetch logs: {e}")
        return []


def get_log(index: int) -> Optional[Dict]:
    """Fetch a specific log by index."""
    if not contract:
        return None

    try:
        user_id_hash, event_type_num, timestamp, meta_hash = contract.functions.getLog(index).call()
        event_types = ["ENROLL", "AUTH_SUCCESS", "AUTH_FAIL", "ADMIN_ACTION"]
        return {
            "index": index,
            "userIdHash": user_id_hash.hex(),
            "eventType": event_types[event_type_num] if event_type_num < len(event_types) else "UNKNOWN",
            "timestamp": timestamp,
            "metaHash": meta_hash.hex(),
        }
    except Exception as e:
        logger.error(f"Failed to fetch log {index}: {e}")
        return None


def verify_metadata(meta_obj: dict, on_chain_meta_hash: str) -> bool:
    """Verify that metadata matches the on-chain hash."""
    meta_json = canonical_json(meta_obj)
    computed_hash = sha256_hex(meta_json)
    return computed_hash == on_chain_meta_hash.replace("0x", "")


def get_total_logs() -> int:
    """Get total number of logs on blockchain."""
    if not contract:
        return 0

    try:
        return contract.functions.totalLogs().call()
    except Exception as e:
        logger.error(f"Failed to get total logs: {e}")
        return 0


def store_metadata(user_id: str, log_index: int, metadata: dict) -> None:
    """Store metadata off-chain (in-memory or database)."""
    if not hasattr(store_metadata, 'storage'):
        store_metadata.storage = {}
    
    key = f"{user_id}:{log_index}"
    store_metadata.storage[key] = {
        "metadata": metadata,
        "stored_at": int(time.time())
    }


def retrieve_metadata(user_id: str, log_index: int) -> Optional[dict]:
    """Retrieve stored metadata off-chain."""
    if not hasattr(store_metadata, 'storage'):
        return None
    
    key = f"{user_id}:{log_index}"
    if key in store_metadata.storage:
        return store_metadata.storage[key]["metadata"]
    return None
