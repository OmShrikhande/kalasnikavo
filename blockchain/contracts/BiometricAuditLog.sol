// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BiometricAuditLog {
    enum EventType { ENROLL, AUTH_SUCCESS, AUTH_FAIL, ADMIN_ACTION }

    struct LogEntry {
        bytes32 userIdHash;   // sha256(user_internal_id or similar)
        EventType eventType;
        uint64 timestamp;     // unix time (server-provided)
        bytes32 metaHash;     // sha256 of detailed JSON stored off-chain
    }

    LogEntry[] public logs;

    event LogRecorded(
        uint256 indexed logIndex,
        bytes32 indexed userIdHash,
        EventType eventType,
        uint64 timestamp,
        bytes32 metaHash
    );

    function addLog(
        bytes32 userIdHash,
        EventType eventType,
        uint64 timestamp,
        bytes32 metaHash
    ) external {
        logs.push(
            LogEntry({
                userIdHash: userIdHash,
                eventType: eventType,
                timestamp: timestamp,
                metaHash: metaHash
            })
        );

        emit LogRecorded(logs.length - 1, userIdHash, eventType, timestamp, metaHash);
    }

    function getLog(uint256 index)
        external
        view
        returns (bytes32, EventType, uint64, bytes32)
    {
        require(index < logs.length, "Index out of range");
        LogEntry memory entry = logs[index];
        return (entry.userIdHash, entry.eventType, entry.timestamp, entry.metaHash);
    }

    function totalLogs() external view returns (uint256) {
        return logs.length;
    }
}
