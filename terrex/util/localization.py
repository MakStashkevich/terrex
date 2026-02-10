from enum import Enum
import json
from pathlib import Path
from typing import Optional

from terrex.structures.net_string import NetworkText, NetworkTextMode


class LocaleType(Enum):
    LEGACY = "Legacy"
    GAME = "Game"
    ITEMS = "Items"
    NPCS = "NPCs"
    PROJECTILES = "Projectiles"
    TOWN = "Town"


def get_translation(
    netstring: NetworkText,
    lang: str = "ru-RU",
    locale_type: LocaleType = LocaleType.LEGACY
) -> str:
    """
    Translates NetString.text as a localization key with substitutions support.
    Example: "LegacyMultiplayer.1" -> "Incorrect password"
    Supports LITERAL, FORMATTABLE, LOCALIZATION_KEY.
    """
    if netstring.mode == NetworkTextMode.LITERAL:
        return netstring.text

    base_text = netstring.text

    if netstring.mode == NetworkTextMode.LOCALIZATION_KEY:
        if "." not in base_text:
            pass  # fallback to base_text
        else:
            parts = base_text.rsplit(".", 1)
            category, subkey = parts
            path = Path(f"locales/{lang}/{lang}.{locale_type.value}.json")
            if path.exists():
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if category in data and subkey in data[category]:
                        base_text = data[category][subkey]
                except (json.JSONDecodeError, KeyError, ValueError):
                    pass

    subs_trans = [get_translation(sub, lang, locale_type) for sub in netstring.substitutions]
    try:
        return base_text.format(*subs_trans)
    except (ValueError, KeyError):
        return base_text