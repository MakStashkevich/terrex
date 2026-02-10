from typing import Any
from dataclasses import is_dataclass
from terrex.structures.net_string import NetworkText


def stringify_network_text(value: "NetworkText") -> dict[str, Any]:  # type: ignore
    from terrex.structures.net_string import NetworkText
    from terrex.util.localization import get_translation

    if not isinstance(value, NetworkText):
        return {}

    return {
        "mode": value.mode.name,
        "key": value.text,
        "translated": get_translation(value),
        "substitutions": [stringify_value(sub) for sub in value.substitutions],
    }


def stringify_value(value: Any) -> Any:
    """
    Recursive stringify for logging/repr: NetworkText -> dict, bytes -> hex, list/dict/dataclass recursive.
    Shared for Packet/NetModule.
    """
    if isinstance(value, NetworkText):
        return stringify_network_text(value)
    if isinstance(value, dict):
        return {key: stringify_value(item) for key, item in value.items()}
    if isinstance(value, (bytes, bytearray)):
        return value.hex()
    if isinstance(value, list):
        return [stringify_value(item) for item in value]
    if is_dataclass(value) or hasattr(value, "__dict__"):
        return {key: stringify_value(getattr(value, key)) for key in vars(value).keys()}
    return value
