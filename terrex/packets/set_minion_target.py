from terrex.packets.base import ClientPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Writer


class SetMinionTarget(ClientPacket):
    id = PacketIds.UPDATE_MINION_TARGET.value

    def __init__(self, player_id: int = 0, minion_attack_target: int = 0):
        self.player_id = player_id
        self.minion_attack_target = minion_attack_target

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_short(self.minion_attack_target)


SetMinionTarget.register()
