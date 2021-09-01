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

def decode_unconnected_ping(data: bytes) -> dict:
    packet: dict = {}
    packet["id"] = data[0]
    packet["client_timestamp"] = struct.unpack(">q", data[1:9])[0]
    assert data[9:25] == MAGIC, "Invalid magic"
    if len(data) <= 9:
        packet["client_guid"] = struct.unpack(">q", data[25:33])[0]
    return packet

def encode_unconnected_ping(packet: dict) -> bytes:
    data: bytes = b""
    data += bytes([packet["id"]])
    data += struct.pack(">q", packet["client_timestamp"])
    data += MAGIC
    if "client_guid" in packet:
        data += struct.pack(">q", packet["client_guid"])
        
def decode_unconnected_pong(data: bytes) -> dict:
    packet: dict = {}
    packet["id"] = data[0]
    packet["client_timestamp"] = struct.unpack(">q", data[1:9])[0]
    packet["server_guid"] = struct.unpack(">q", data[9:17])[0]
    assert data[17:33] == MAGIC, "Invalid magic"
    packet["data"] = data[33:]
    return packet

def encode_unconnected_pong(packet: dict) -> bytes:
    data: bytes = b""
    data += bytes([packet["id"]])
    data += struct.pack(">q", packet["client_timestamp"])
    data += struct.pack(">q", packet["server_guid"]) 
    data += MAGIC
    data += packet["data"]
