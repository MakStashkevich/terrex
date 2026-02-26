from terrex.id import MessageID
from terrex.net.streamer import Writer
from terrex.packet.base import ClientPacket


class MurderSomeoneElsesPortal(ClientPacket):
    id = MessageID.MurderSomeoneElsesPortal

    def __init__(self, projectile_owner: int = 0, projectile_ai: int = 0):
        self.projectile_owner = projectile_owner
        self.projectile_ai = projectile_ai

    def write(self, writer: Writer):
        writer.write_ushort(self.projectile_owner)
        writer.write_byte(self.projectile_ai)
