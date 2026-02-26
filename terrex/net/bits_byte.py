class BitsByte:
    def __init__(self, value: int = 0):
        self.value = value & 0xFF  # byte limit

    def __getitem__(self, index: int) -> bool:
        if not 0 <= index < 8:
            raise IndexError("Index must be 0-7")
        return bool((self.value >> index) & 1)

    def __setitem__(self, index: int, val: bool):
        if not 0 <= index < 8:
            raise IndexError("Index must be 0-7")
        if val:
            self.value |= 1 << index
        else:
            self.value &= ~(1 << index)

    def __int__(self) -> int:
        return self.value

    def __repr__(self):
        return f"BitsByte({self.value:08b})"
