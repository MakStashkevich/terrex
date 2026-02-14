from dataclasses import is_dataclass
from enum import Enum
from typing import Any

from terrex.structures.localization.network_text import NetworkText


def stringify_network_text(value: Any, depth: int = 0, max_depth: int = 20, seen: set = None) -> dict[str, Any]:
    if seen is None:
        seen = set()

    from terrex.structures.localization.network_text import NetworkText
    from terrex.util.localization import get_translation

    if not isinstance(value, NetworkText):
        return repr(value)

    if depth > max_depth:
        return {
            "mode": "<truncated>",
            "key": "<truncated>",
            "translated": "<truncated>",
            "substitutions": [],
        }

    obj_id = id(value)
    seen.add(obj_id)
    try:
        return {
            "mode": value.mode.name,
            "key": value.text,
            "translated": get_translation(value),
            "substitutions": [stringify_value(sub, depth + 1, max_depth, seen) for sub in value.substitutions],
        }
    finally:
        seen.remove(obj_id)


def stringify_value(value: Any, depth: int = 0, max_depth: int = 20, seen: set = None) -> Any:
    """
    Recursive stringify for logging/repr: NetworkText -> dict, bytes -> hex, list/dict/dataclass recursive.
    Shared for Packet/NetModule. Supports cycle detection and max depth truncation.
    """
    if seen is None:
        seen = set()
    obj_id = id(value)
    if obj_id in seen:
        return "<cycle>"
    if depth > max_depth:
        return f"<truncated at depth {depth}>"
    seen.add(obj_id)
    try:
        if isinstance(value, NetworkText):
            return stringify_network_text(value, depth, max_depth, seen)
        if isinstance(value, Enum):
            return f"{value.name}({value.value})"
        if isinstance(value, dict):
            return {str(key): stringify_value(item, depth + 1, max_depth, seen) for key, item in value.items()}
        if isinstance(value, (bytes, bytearray)):
            return value.hex()
        if isinstance(value, list):
            return [stringify_value(item, depth + 1, max_depth, seen) for item in value]
        if is_dataclass(value) or hasattr(value, "__dict__"):
            return {str(key): stringify_value(getattr(value, key), depth + 1, max_depth, seen) for key in vars(value).keys()}
        return repr(value)
    finally:
        seen.remove(obj_id)
