import time

from terrex.event.event import Event
from terrex.net import module
from terrex.player.player import Player
from terrex.net.protocol import PROTOCOLS
from terrex.net.chat_command import ChatCommand
from terrex.world.world import World

from . import client, packet
from .event import EventManager

# The latest supported version of Terraria
TERRARIA_VERSION = (1, 4, 5, 5)


class Terrex:
    """A class that handles basic functions of a terraria bot like movement and login"""

    # Defaults to 7777, because that is the default port for the server
    def __init__(
        self,
        ip,
        port: int = 7777,
        server_password: str = "",
        version: tuple = TERRARIA_VERSION,
        player: Player | None = None,
    ):
        super().__init__()

        if version not in PROTOCOLS:
            version_str = f"v{'.'.join(map(str, version))}"
            raise ValueError(f"Protocol for Terraria version {version_str} not supported")
        protocol = PROTOCOLS[version]

        self.world = World()
        self.player = player or Player()

        self.evman = EventManager()

        self.client = client.Client(ip, port, protocol, server_password, self.player, self.world, self.evman)

    def send_message(self, text: str):
        if self.player.logged_in:
            self.client.send(
                packet.NetModules(
                    module=module.NetTextModule(
                        chat_command_id=ChatCommand.SayChat,
                        text=text,
                    ),
                )
            )

    def get_event_manager(self):
        return self.evman

    def on(self, event_id: Event):
        return self.evman.on_event(event_id)

    def stop(self):
        self.client.stop()

    def __enter__(self):
        self.client.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def run_until_disconnected(self):
        try:
            while self.client.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Stopping bot...")
        self.stop()
