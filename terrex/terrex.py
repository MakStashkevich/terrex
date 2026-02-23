import asyncio
from collections.abc import Callable
import inspect
import threading
from typing import Awaitable, ParamSpec, TypeVar, Union

import concurrent

from terrex.client import Client
from terrex.event.dispatcher import Dispatcher
from terrex.event.filter.base import EventFilter
from terrex.net import module
from terrex.net.enum.teleport_pylon_operation import TeleportPylonOperation
from terrex.net.enum.teleport_pylon_type import TeleportPylonType
from terrex.net.enum.teleport_request_type import TeleportRequestType
from terrex.net.enum.teleport_type import TeleportType
from terrex.net.structure.vec2 import Vec2
from terrex.player.player import Player
from terrex.net.protocol import PROTOCOLS
from terrex.net.enum.chat_command import ChatCommand
from terrex.world.world import World

from . import packet
from .event import EventManager

# The latest supported version of Terraria
TERRARIA_VERSION = (1, 4, 5, 5)

E = TypeVar("E")
P = ParamSpec("P")
T = TypeVar("T")


class Terrex:
    """A class that handles basic functions of a terraria bot like movement and login"""

    _async_thread_tasks: set[asyncio.Task] = set()
    loop: asyncio.AbstractEventLoop | None = None
    _loop_thread_id: int | None = None

    world: World
    player: Player
    evman: EventManager
    client: Client

    # Defaults to 7777, because that is the default port for the server
    def __init__(
        self,
        ip,
        port: int = 7777,
        server_password: str = "",
        version: tuple = TERRARIA_VERSION,
        player: Player | None = None,
    ):
        if version not in PROTOCOLS:
            version_str = f"v{'.'.join(map(str, version))}"
            raise ValueError(f"Protocol for Terraria version {version_str} not supported")
        protocol = PROTOCOLS[version]

        self.world = World()
        self.player = player or Player()

        dispatcher = Dispatcher(self)
        self.evman = EventManager(dispatcher)

        self.client = Client(ip, port, protocol, server_password, self)

    async def send_message(self, text: str, wait: bool = False):
        """
        Send a chat message to the server.

        Args:
            text (str): The message text to send.
            wait (bool, optional): Whether to wait for the packet to be sent. Defaults to False.

        Example:
            await terrex.send_message("Hello, world!")
        """
        if not self.player.logged_in:
            return
        await self.client.send(
            packet.NetModules(
                module=module.NetTextModule(
                    chat_command_id=ChatCommand.SayChat,
                    text=text,
                ),
            ),
            wait=wait,
        )

    async def teleport(self, position: Vec2, type: TeleportType = TeleportType.RecallPotion, pylon_type: TeleportPylonType | None = None) -> None:
        """
        Teleport the player to a specific position using various teleport methods.

        Args:
            position (Vec2): The target position to teleport to.
            type (TeleportType, optional): The type of teleport. Defaults to RecallPotion.
            pylon_type (TeleportPylonType | None, optional): Required for TeleportationPylon type.

        Raises:
            NotImplementedError: For unsupported teleport types like TeleporterTile, Portal, etc.
            ValueError: If pylon_type is None for TeleportationPylon.

        Example:
            # Recall potion teleport
            await terrex.teleport(Vec2(100, 200))

            # Pylon teleport
            await terrex.teleport(Vec2(100, 200), TeleportType.TeleportationPylon, TeleportPylonType.Forest)
        """
        if not self.player.logged_in:
            return
        match type:
            case TeleportType.TeleporterTile:
                raise NotImplementedError("Use HitSwitch() packet to enable portal tile")
            case TeleportType.RodOfDiscord:
                # todo: not tested
                await self.client._teleport_entity(position, type, player_teleport=True)
                return
            case TeleportType.TeleportationPotion:
                await self.client._request_teleport(type=TeleportRequestType.TeleportationPotion)
                return
            case TeleportType.RecallPotion:
                await self.client._teleport_entity(position, type, player_teleport=True)
                return
            case TeleportType.Portal:
                raise NotImplementedError("Deprecated, use TeleportPlayerThroughPortal() packet")
            case TeleportType.MagicConch:
                await self.client._request_teleport(type=TeleportRequestType.MagicConch)
                return
            case TeleportType.DebugTeleport:
                raise NotImplementedError("Never used")
            case TeleportType.DemonConch:
                await self.client._request_teleport(type=TeleportRequestType.DemonConch)
                return
            case TeleportType.PotionOfReturn:
                # todo: not tested
                await self.client._teleport_entity(position, type, player_teleport=True)
                return
            case TeleportType.TeleportationPylon:
                if not pylon_type:
                    raise ValueError("Pylon type is required")
                await self.client._request_teleport_pylon(position.x, position.y, pylon_type)
                return
            case TeleportType.QueenSlimeHook:
                await self.client._teleport_entity(position, type, player_teleport=False)  # hook is not player teleporter
                return
            case TeleportType.ShellphoneSpawn:
                await self.client._request_teleport(type=TeleportRequestType.Shellphone_Spawn)
                return
            case TeleportType.ShimmerTownNPCTransform:
                raise NotImplementedError("Only for NPC server logic")
            case TeleportType.MysticFrog:
                raise NotImplementedError("Only for NPC server logic")
            case TeleportType.NoEffect:
                raise NotImplementedError("Only for NPC server logic")

    def get_event_manager(self):
        return self.evman

    def on(self, filter: EventFilter):
        return self.evman.on_event(filter)

    def _task_done_callback(self, task: asyncio.Task):
        """
        Removes a completed task from the internal task set
        and safely retrieves any exception to prevent
        'Task exception was never retrieved' warnings.
        """
        self._async_thread_tasks.discard(task)

        if task.cancelled():
            return

        # Retrieve exception
        exc = task.exception()
        if exc:
            print(f"Async task error: {exc}")

    def call_async(
        self,
        func: Callable[P, Union[T, Awaitable[T]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> concurrent.futures.Future[T]:
        """
        Must be called from a different thread than the event loop.
        Executes `func` (sync or async) inside the loop.

        Returns:
            concurrent.futures.Future[T]
        """

        if not self.client.running:
            raise RuntimeError("Client is not running")

        loop: asyncio.AbstractEventLoop = self.loop
        loop_thread_id: int = self._loop_thread_id
        current_thread_id: int = threading.get_ident()

        if current_thread_id == loop_thread_id:
            raise RuntimeError("call_async must not be called from the event loop thread")

        if inspect.iscoroutinefunction(func):
            coro: Awaitable[T] = func(*args, **kwargs)
        else:

            async def wrapper() -> T:
                return func(*args, **kwargs)

            coro = wrapper()

        future: concurrent.futures.Future[T] = asyncio.run_coroutine_threadsafe(coro, loop)
        return future

    async def stop(self):
        await self.client.stop()

        tasks_to_cancel = list(self._async_thread_tasks)
        for t in tasks_to_cancel:
            t.cancel()

    async def __aenter__(self):
        self.loop = asyncio.get_running_loop()
        self._loop_thread_id = threading.get_ident()

        await self.client.connect()
        while not self.client.connected_to_server and self.client.running:
            await asyncio.sleep(0.05)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

    async def run_until_disconnected(self):
        try:
            while self.client.running:
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            pass
        finally:
            print("Stopping bot...")
            await self.stop()
