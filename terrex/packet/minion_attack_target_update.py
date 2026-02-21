from terrex.packet.base import ClientPacket
from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer


class MinionAttackTargetUpdate(ClientPacket):
    id = MessageID.MinionAttackTargetUpdate

    def __init__(self, player_id: int = 0, minion_target: int = 0):
        self.player_id = player_id
        self.minion_target = minion_target

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.minion_target = reader.read_short()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_short(self.minion_target)
