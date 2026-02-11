from typing import Tuple, Dict

PROTOCOLS: Dict[Tuple[int, ...], int] = {
    # not tested
    (1, 4, 4, 9): 279,
    (1, 4, 5, 0): 313,
    (1, 4, 5, 1): 314,
    (1, 4, 5, 2): 315,
    # 100% working fine
    (1, 4, 5, 3): 316,
    (1, 4, 5, 4): 317,
    (1, 4, 5, 5): 318,
}
"""Terraria protocols by version. The key is the version tuple (major, minor, build, revision), the value is the protocol number."""
