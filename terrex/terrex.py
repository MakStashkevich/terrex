import asyncio
from collections.abc import Callable
import inspect
import threading
from typing import Awaitable, ParamSpec, TypeVar, Union

import concurrent

from terrex.client import Client
from terrex.event.event import Event
from terrex.net import module
from terrex.player.player import Player
from terrex.net.protocol import PROTOCOLS
from terrex.net.enum.chat_command import ChatCommand
from terrex.world.world import World

from . import packet
from .event import EventManager

# The latest supported version of Terraria
TERRARIA_VERSION = (1, 4, 5, 5)

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

        self.evman = EventManager()

        self.client = Client(ip, port, protocol, server_password, self.player, self.world, self.evman)

    async def send_message(self, text: str, wait: bool = False):
        if self.player.logged_in:
            await self.client.send(
                packet.NetModules(
                    module=module.NetTextModule(
                        chat_command_id=ChatCommand.SayChat,
                        text=text,
                    ),
                ),
                wait=wait
            )

    def get_event_manager(self):
        return self.evman

    def on(self, event_id: Event):
        return self.evman.on_event(event_id)

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
