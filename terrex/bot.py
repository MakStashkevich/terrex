from terrex.protocols import PROTOCOLS
from . import packets
from . import client

from terrex.data.player import Player
from terrex.data.world import World
from .events import Events, EventManager


class Terrex(object):
    """A class that handles basic functions of a terraria bot like movement and login"""

    # Defaults to 7777, because that is the default port for the server
    def __init__(self, ip, port=7777, protocol=PROTOCOLS[(1, 4, 5, 4)], name="Terrex"):
        super(Terrex, self).__init__()

        self.world = World()
        self.player = Player(name)

        self.evman = EventManager()

        self.client = client.Client(
            ip, port, protocol, self.player, self.world, self.evman
        )

        # self.evman.method_on_event(Events.PlayerID, self.received_player_id)
        # self.evman.method_on_event(Events.Initialized, self.initialized)
        # self.evman.method_on_event(Events.Login, self.logged_in)
        # self.evman.method_on_event(Events.ItemOwnerChanged, self.item_owner_changed)
        # self.event_manager.method_on_event(events.Events.)

    def start(self):
        self.client.connect()

    def item_owner_changed(self, id, data):
        if self.player.logged_in:
            self.client.send(packets.PlayerHp(id, data[0], data[1]))

    def received_player_id(self, event_id, data):
        self.client.send(packets.PlayerInfo(self.player))
        self.client.send(packets.Packet10(self.player))
        self.client.send(packets.Packet2A(self.player))  # player mana
        self.client.send(packets.Packet32(self.player))  # update player buff
        for i in range(0, 83):
            self.client.send(packets.Packet5(self.player, i))  # player inventory slot
        self.client.send(packets.Packet6())  # request world data

    def initialized(self, event, data):
        self.client.send(
            packets.Packet8(self.player, self.world)
        )  # REQUEST_ESSENTIAL_TILES

    def logged_in(self, event, data):
        self.client.send(packets.PacketC(self.player, self.world))  # SPAWN_PLAYER

    def message(self, msg, color=None):
        if self.player.logged_in:
            if color:
                hex_code = "%02x%02x%02x" % color
                msg = "[c/" + hex_code + ":" + msg + "]"
            # self.client.send(packets.Packet19(self.player, msg))

    def get_event_manager(self):
        return self.evman

    def stop(self):
        self.client.stop()
