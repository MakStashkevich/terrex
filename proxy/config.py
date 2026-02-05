from typing import Optional, BinaryIO
import threading
from proxy.parser import IncrementalParser


class Config:
    def __init__(self):
        self.server_parser: IncrementalParser = IncrementalParser()
        self.client_parser: IncrementalParser = IncrementalParser()
        self.server_traffic: Optional[BinaryIO] = open("server-traffic.bin", "wb")
        self.client_traffic: Optional[BinaryIO] = open("client-traffic.bin", "wb")
        self.flush_traffic: list[bool] = [False, False]
        self.dbg_in_tags: list[bool] = [True] * 256
        self.dbg_out_tags: list[bool] = [True] * 256
        self.lock: threading.Lock = threading.Lock()


config = Config()
