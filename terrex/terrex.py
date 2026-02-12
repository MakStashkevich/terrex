from terrex import structures
from terrex.protocols import PROTOCOLS
from terrex.structures.chat.chat_command import ChatCommand
from terrex.structures.localization.network_text import NetworkText
from . import packets
from . import client

from terrex.entity.player import Player
from terrex.world.world import World
from .events import EventManager

# The latest supported version of Terraria
TERRARIA_VERSION = (1, 4, 5, 5)


class Terrex(object):
    """A class that handles basic functions of a terraria bot like movement and login"""

    # Defaults to 7777, because that is the default port for the server
    def __init__(
        self,
        ip,
        port=7777,
        server_password: str = "",
        version=TERRARIA_VERSION,
        player=Player(),
    ):
        super(Terrex, self).__init__()

        if version not in PROTOCOLS:
            version_str = f"v{'.'.join(map(str, version))}"
            raise ValueError(
                f"Protocol for Terraria version {version_str} not supported"
            )
        protocol = PROTOCOLS[version]

        self.world = World()
        self.player = player

        self.evman = EventManager()

        self.client = client.Client(
            ip, port, protocol, server_password, self.player, self.world, self.evman
        )

    def start(self):
        self.client.connect()

    def send_message(self, text: str):
        if self.player.logged_in:
            self.client.send(
                packets.LoadNetModule(
                    module=structures.NetTextModule(
                        chat_command_id=ChatCommand.SayChat,
                        text=text,
                    ),
                )
            )

    def get_event_manager(self):
        return self.evman

    def stop(self):
        self.client.stop()
