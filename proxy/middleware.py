import struct

from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import Packet
from terrex.packet.update_player_luck_factors import UpdatePlayerLuckFactors


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

    # if packet_id == MessageID.DamageNPC:
    #     packet = DamageNPC()
    #     packet.read(reader)
    #     packet.damage = 10000
    #     packet.knockback = 50
    #     packet.crit = True

    if packet_id == MessageID.UpdatePlayerLuckFactors:
        packet = UpdatePlayerLuckFactors()
        packet.read(reader)
        packet.has_garden_gnome_nearby = True
        packet.ladybug_luck_time_left = 10
        packet.luck_potion = 10
        packet.torch_luck = 10

    if packet:
        writer = Writer()
        writer.write_byte(packet.id)
        packet.write(writer)
        payload = writer.bytes()

    return payload
