import json
from enum import Enum
from pathlib import Path

from terrex.localization.network_text import NetworkText, NetworkTextMode


class LocaleType(Enum):
    LEGACY = "Legacy"
    GAME = "Game"
    ITEMS = "Items"
    NPCS = "NPCs"
    PROJECTILES = "Projectiles"
    TOWN = "Town"


def get_translation(
    net_text: NetworkText, lang: str = "en-US", locale_type: LocaleType = LocaleType.LEGACY
) -> str:
    """
    Translates NetString.text as a localization key with substitutions support.
    Example: "LegacyMultiplayer.1" -> "Incorrect password"
    Supports LITERAL, FORMATTABLE, LOCALIZATION_KEY.
    """
    if net_text.mode == NetworkTextMode.LITERAL:
        return net_text.text

    base_text = net_text.text

    if net_text.mode == NetworkTextMode.LOCALIZATION_KEY:
        if "." not in base_text:
            pass  # fallback to base_text
        else:
            parts = base_text.rsplit(".", 1)
            category, subkey = parts
            path = Path(f"locale/{lang}/{lang}.{locale_type.value}.json")
            if path.exists():
                try:
                    with open(path, encoding="utf-8") as f:
                        data = json.load(f)
                    if category in data and subkey in data[category]:
                        base_text = data[category][subkey]
                except (json.JSONDecodeError, KeyError, ValueError):
                    pass

    subs_trans = [get_translation(sub, lang, locale_type) for sub in net_text.substitutions]
    try:
        return base_text.format(*subs_trans)
    except (ValueError, KeyError):
        return base_text
