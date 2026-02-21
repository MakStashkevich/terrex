from terrex.packet.base import SyncPacket
from terrex.net.bits_byte import BitsByte
from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer


class SyncPlayerZone(SyncPacket):
    id = MessageID.SyncPlayerZone

    def __init__(
        self,
        player_id: int = 0,
        zone1: BitsByte | None = None,
        zone2: BitsByte | None = None,
        zone3: BitsByte | None = None,
        zone4: BitsByte | None = None,
        zone5: BitsByte | None = None,
        town_npc_count: int = 0,
    ):
        self.player_id = player_id
        self.zone1 = zone1 or BitsByte()
        self.zone2 = zone2 or BitsByte()
        self.zone3 = zone3 or BitsByte()
        self.zone4 = zone4 or BitsByte()
        self.zone5 = zone5 or BitsByte()
        self.town_npc_count = town_npc_count

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.zone1 = BitsByte(reader.read_byte())
        self.zone2 = BitsByte(reader.read_byte())
        self.zone3 = BitsByte(reader.read_byte())
        self.zone4 = BitsByte(reader.read_byte())
        self.zone5 = BitsByte(reader.read_byte())
        self.town_npc_count = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_byte(int(self.zone1))
        writer.write_byte(int(self.zone2))
        writer.write_byte(int(self.zone3))
        writer.write_byte(int(self.zone4))
        writer.write_byte(int(self.zone5))
        writer.write_byte(self.town_npc_count)

    async def handle(self, world, player, evman):
        player.zone.update(zone1=self.zone1, zone2=self.zone2, zone3=self.zone3, zone4=self.zone4, zone5=self.zone5)
