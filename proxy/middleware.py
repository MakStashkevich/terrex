import struct

from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.packets.npc_strike import NpcStrike
from terrex.packets.update_player_luck import UpdatePlayerLuck
from terrex.util.streamer import Reader, Writer


class AnyPacket(Packet):
    pass


def client_packet_middleware(data: bytes) -> bytes:
    if not data:
        return data

    result = bytearray()
    offset = 0
    total_length = len(data)
    while offset + 2 <= total_length:
        packet_length = struct.unpack_from("<H", data, offset)[0]
        if packet_length <= 0:
            result.extend(data[offset:])
            return bytes(result)
        packet_end = offset + packet_length
        if packet_end > total_length:
            result.extend(data[offset:])
            return bytes(result)

        payload = data[offset + 2 : packet_end]
        if payload:
            payload = rewrite_packet(payload)
            packet_length = 2 + len(payload)

        header = struct.pack("<H", packet_length)
        result.extend(header)
        result.extend(payload)
        offset = packet_end

    result.extend(data[offset:])
    return bytes(result)


def rewrite_packet(payload: bytes) -> bytes:
    packet = None
    packet_id = payload[0]
    reader = Reader(payload[1:])

    # if packet_id == PacketIds.NPC_STRIKE.value:
    #     packet = NpcStrike()
    #     packet.read(reader)
    #     packet.damage = 10000
    #     packet.knockback = 50
    #     packet.crit = True

    if packet_id == PacketIds.UPDATE_PLAYER_LUCK_FACTORS.value:
        packet = UpdatePlayerLuck()
        packet.read(reader)
        packet.has_garden_gnome_nearby = True
        packet.ladybug_luck_time_remaining = 10
        packet.luck_potion = 10
        packet.torch_luck = 10

    if packet:
        writer = Writer()
        writer.write_byte(packet.id)
        packet.write(writer)
        payload = writer.bytes()

    return payload
