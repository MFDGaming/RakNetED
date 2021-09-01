# Copyright Alexander Argentakis (MFDGaming). This
# file is licensed under the GPLv2 license. If you
# dont have a copy of this license you may get it at
# https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html

import struct

MAGIC = bytes([
    0x00, 0xff, 0xff, 0x00,
    0xfe, 0xfe, 0xfe, 0xfe,
    0xfd, 0xfd, 0xfd, 0xfd,
    0x12, 0x34, 0x56, 0x78
])

PACKET_IDS = {
    "Unconnected Ping": 0x01,
    "Unconnected Ping Open Connections": 0x02,
    "Unconnected Pong": 0x1c,
    "Open Connection Request 1": 0x05,
    "Incompatible Protocol Version": 0x19,
    "Open Connection Reply 1": 0x06,
    "Open Connection Request 2": 0x07,
    "Open Connection Reply 2": 0x08,
    "Connection Request": 0x09,
    "Connection Request Accepted": 0x10,
    "New Incoming Connection": 0x13,
    "ACK": 0xc0,
    "NAK": 0xa0
}

def decode_unconnected_ping(
    data: bytes,
    protocol_version: int,
    has_open_connections: bool=False
) -> dict:
    packet_id: int = PACKET_IDS[
        "Unconnected Ping Open Connections"
        if has_open_connections else
        "Unconnected Ping"
    ]
    packet: dict = {}
    assert data[0] == packet_id, "Invalid packet id"
    packet["ID"] = data[0]
    packet["Client Timestamp"] = struct.unpack(">q", data[1:9])[0]
    assert data[9:25] == MAGIC, "Invalid magic"
    if protocol_version >= 8:
        packet["Client GUID"] = struct.unpack(">q", data[25:33])[0]
    return packet
