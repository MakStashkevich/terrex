from collections import deque
from threading import Lock
from typing import cast


class SetFactory:
    def __init__(self, size: int):
        if size == 0:
            raise ValueError("size cannot be 0")
        self._size = size
        self._queue_lock = Lock()
        self._int_buffer_cache: deque[list[int]] = deque()
        self._ushort_buffer_cache: deque[list[int]] = deque()
        self._bool_buffer_cache: deque[list[bool]] = deque()
        self._float_buffer_cache: deque[list[float]] = deque()

    def _get_buffer(self, cache: deque, dtype):
        with self._queue_lock:
            if cache:
                return cache.popleft()
            return [dtype()] * self._size

    def _recycle_buffer(self, buffer, dtype):
        with self._queue_lock:
            if dtype is bool:
                self._bool_buffer_cache.append(buffer)
            elif dtype is int:
                self._int_buffer_cache.append(buffer)
            elif dtype is float:
                self._float_buffer_cache.append(buffer)

    def create_bool_set(self, default_state: bool = False, *types: int) -> list[bool]:
        arr = cast(list[bool], self._get_buffer(self._bool_buffer_cache, bool))
        for i in range(self._size):
            arr[i] = default_state
        for t in types:
            if 0 <= t < self._size:
                arr[t] = not default_state
        return arr

    def create_int_set(self, default_state: int = -1, *inputs: int) -> list[int]:
        if len(inputs) % 2 != 0:
            raise ValueError("inputs length must be even")
        arr = cast(list[int], self._get_buffer(self._int_buffer_cache, int))
        for i in range(self._size):
            arr[i] = default_state
        for j in range(0, len(inputs), 2):
            idx = inputs[j]
            val = inputs[j + 1]
            if 0 <= idx < self._size:
                arr[idx] = val
        return arr

    def create_float_set(self, default_state: float, *inputs: float) -> list[float]:
        if len(inputs) % 2 != 0:
            raise ValueError("inputs length must be even")
        arr = cast(list[float], self._get_buffer(self._float_buffer_cache, float))
        for i in range(self._size):
            arr[i] = default_state
        for j in range(0, len(inputs), 2):
            idx = int(inputs[j])
            val = inputs[j + 1]
            if 0 <= idx < self._size:
                arr[idx] = val
        return arr

    def create_ushort_set(self, default_state: int, *inputs: int) -> list[int]:
        if len(inputs) % 2 != 0:
            raise ValueError("inputs length must be even")
        arr = cast(list[int], self._get_buffer(self._ushort_buffer_cache, int))
        for i in range(self._size):
            arr[i] = default_state
        for j in range(0, len(inputs), 2):
            idx = inputs[j]
            val = inputs[j + 1]
            if 0 <= idx < self._size:
                arr[idx] = val
        return arr

    def create_custom_set(self, default_state, *inputs) -> list:
        if len(inputs) % 2 != 0:
            raise ValueError("inputs length must be even")
        arr = [default_state] * self._size
        for j in range(0, len(inputs), 2):
            key = inputs[j]
            val = inputs[j + 1]
            idx = int(key)
            if 0 <= idx < self._size:
                arr[idx] = val
        return arr

    def recycle(self, buffer, dtype=bool):
        if not buffer:
            return
        self._recycle_buffer(buffer, dtype)
