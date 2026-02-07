from typing import Optional, BinaryIO, TextIO
import threading
from proxy.parser import IncrementalParser


class Config:
    def __init__(self):
        self.server_parser: IncrementalParser = IncrementalParser()
        self.client_parser: IncrementalParser = IncrementalParser()
        self.server_traffic_bin: Optional[BinaryIO] = None
        self.client_traffic_bin: Optional[BinaryIO] = None
        self.server_traffic_txt: Optional[TextIO] = None
        self.client_traffic_txt: Optional[TextIO] = None
        self.both_traffic_txt: Optional[TextIO] = None
        self.flush_bin: list[bool] = [False, False]
        self.flush_txt: list[bool] = [False, False]
        self.flush_both_txt: bool = False
        self.dbg_in_tags: list[bool] = [True] * 256
        self.dbg_out_tags: list[bool] = [True] * 256
        self.lock: threading.Lock = threading.Lock()


config = Config()
