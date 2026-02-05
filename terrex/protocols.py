from typing import Tuple, Dict

PROTOCOLS: Dict[Tuple[int, ...], int] = {
    (1, 4, 4, 9): 279,
    (1, 4, 5, 4): 316,  # Версия Terraria 1.4.5.4
}
"""Протоколы Terraria по версиям. Ключ - tuple версии (major, minor, build, revision), значение - номер протокола."""
