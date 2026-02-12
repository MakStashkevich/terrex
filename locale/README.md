# Terraria Locales Extractor

## Purpose

The `terraria_localization.py` script extracts localization resources from the Terraria executable (`Terraria.exe`) and converts them into pretty-printed JSON files. This is essential for the TerreX project to access and translate game strings, such as server disconnect reasons, item names, NPC dialogues, and other localized content.

It enables seamless integration of multilingual support, allowing the project to display translated messages from the game server.

## Requirements

Install the required package:

```bash
pip install dnfile
```

## How It Works

1. **Resource Parsing**: The script parses embedded resources in the Terraria executable using tools like Python's resource extraction libraries (e.g., for PyInstaller-packed binaries).
2. **Localization Extraction**: Identifies and extracts specific localization files (or all available ones) for languages like `en-US` and `ru-RU`.
3. **Conversion to JSON**: Transforms the binary localization data into human-readable, pretty-printed JSON format with key-value pairs for easy lookup and modification.

## Running the Script

```bash
python locale/terraria_localization.py /path/to/Terraria.exe locale/ false ru-RU en-US
```

Dumps only the specified languages (`ru-RU`, `en-US`).

```bash
python locale/terraria_localization.py /path/to/Terraria.exe locale/ true
```

Dumps **all** available languages.

**Arguments:**
- `<exe_path>`: Full path to `Terraria.exe`
- `<output_dir>`: Output directory (e.g., `locale/`)
- `<dump_all>`: `true` (dump all langs) or `false` (only listed langs)
- `[lang1 lang2 ...]`: Optional specific languages (e.g., `ru-RU en-US zh-CN`)

**Common Paths to `Terraria.exe`:**

**macOS (Steam):**
- `~/Library/Application Support/Steam/steamapps/common/Terraria/Terraria.app/Contents/Resources/Terraria.exe`
- `/Volumes/{disk_name}/SteamLibrary/steamapps/common/Terraria/Terraria.app/Contents/Resources/Terraria.exe` (external drive)

**Windows:**
- `C:\\Program Files (x86)\\Steam\\steamapps\\common\\Terraria\\Terraria.exe`

## Generated Files

The script creates language-specific directories under `locale/`, such as:
- `locale/en-US/`
  - [`en-US.Game.json`](en-US/en-US.Game.json)
  - [`en-US.Items.json`](en-US/en-US.Items.json)
  - [`en-US.NPCs.json`](en-US/en-US.NPCs.json)
  - [`en-US.Projectiles.json`](en-US/en-US.Projectiles.json)
  - [`en-US.Legacy.json`](en-US/en-US.Legacy.json)
  - [`en-US.Town.json`](en-US/en-US.Town.json)
  - [`en-US.json`](en-US/en-US.json)

Similar structure for `ru-RU/` and other supported languages.

Each JSON file contains nested objects mapping localization keys to their translated strings.

## Usage

Load the locales using [`terrex/util/localization.py`](../terrex/util/localization.py) and use the `get_translation(key)` function to retrieve translated strings from server packets.

**Example** from [`terrex/client.py`](../terrex/client.py):

```python
if packet_id == 2 and isinstance(packet, packets.Disconnect):
    print(f"[READ] Packet ID: 0x{packet_id:02X}. Disconnect with reason: {get_translation(packet.reason)}")
    self.stop()
    continue
```

- `get_translation(packet.reason)` looks up the disconnect reason key (e.g., from `Game.json`) and returns the localized string (English or Russian, depending on loaded locale).
- Supports fallback to English if translation is missing.
- Ideal for logging, UI display, bots, proxies, and any component handling game/server messages.

To switch languages, update the locale loader in [`terrex/util/localization.py`](../terrex/util/localization.py).