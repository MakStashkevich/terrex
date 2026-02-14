# TerrariaPyGen

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/makstashkevich/terrex/blob/master/helper/LICENSE.txt)

**TerrariaPyGen** is a powerful auto-generator for Python classes and enums from decompiled Terraria C# sources (namespace `Terraria.ID`). It converts static ID classes (e.g., `ItemID`, `TileID`, `NPCID`) into convenient Python structures ready for use in the Terrex project.

Generates files into the `terrex/structures/id/` directory, supporting nested classes, obsolete constants, `[Old]` comments, and complex `SetFactory` for Terraria Sets.

## ✨ Features

- 🔍 **Precise C# Parsing**: Extracts `public const` (int, ushort, byte, etc.), `readonly Count`, static assignments.
- 📁 **Nested Classes**: Automatic handling of nested classes (e.g., `TileID.Sets`).
- 🗑️ **Obsolete Handling**: Marks `[Obsolete]` constants as comments (`# Name = value`).
- 📝 **Comments**: Preserves `[Old("description")]` as `# description`.
- 🏭 **SetFactory**: Generates Python equivalents for `Factory.CreateBoolSet()`, `CreateIntSet()`, arrays `new int[]`.
- ⚙️ **Enum vs Class**: Uses `IntEnum` for pure numeric IDs, plain `class` for mixed.
- 🔄 **CLI Interface**: Single-file script with recursive folder processing.
- 📊 **Validation**: Only allowed classes from `ALLOWED_CLASSES`.

## 📦 Installation

The script is self-contained and depends only on Python standard library + `terrex` (for `TERRARIA_VERSION` and `SetFactory`).

Place `.cs` files into `folder_with_cs_files/` (or specify path).

## 🚀 Usage

### Generate Single File
```bash
python helper/TerrariaPyGen.py folder_with_cs_files/ArmorIDs.cs
```
Output: `terrex/structures/id/ArmorIDs.py`

### Recursive Generation
```bash
python helper/TerrariaPyGen.py folder_with_cs_files/ --recursive
```
Processes all `.cs` files up to depth 3.

### Example Output
```
Saved to terrex/structures/id/ArmorIDs.py
Done: 1/1 successful
```

## 📋 Supported Classes (`Terraria.ID`)

| Class | Example |
|-------|---------|
| `ArmorIDs` | `Head`, `Body`, `Legs`, `Count` |
| `TileID` | `Grass`, `Stone`, `Sets.RoomNeeds` |
| `ItemID` | `Wood`, `IronBar`, `Sets` |
| ... | [Full list in code](TerrariaPyGen.py) |

Full list in [`ALLOWED_CLASSES`](TerrariaPyGen.py#22).

## 🔍 Example Generated Code

**Input:** `Terraria/ID/MessageID.cs` (snippet)
```csharp
using System;
using Terraria.Utilities;

namespace Terraria.ID
{
	public class MessageID
	{
		public const byte NeverCalled = 0;

		public const byte Hello = 1;

		public const byte Kick = 2;

		public const byte PlayerInfo = 3;

		public const byte SyncPlayer = 4;

		public const byte SyncEquipment = 5;

		public const byte RequestWorldData = 6;

		public const byte WorldData = 7;

		public const byte SpawnTileData = 8;

		public const byte StatusTextSize = 9;

		public const byte TileSection = 10;

		[Old("Deprecated. Framing happens as needed after TileSection is sent.")]
		public const byte TileFrameSection = 11;

		public const byte PlayerSpawn = 12;

		public const byte PlayerControls = 13;

		public const byte PlayerActive = 14;

		[Old("Deprecated.")]
		public const byte Unknown15 = 15;

		public const byte PlayerLifeMana = 16;
    }
}
```

**Output:** `terrex/structures/id/MessageID.py`
```python
from enum import IntEnum, auto

class MessageID(IntEnum):
    NeverCalled = 0
    Hello = 1
    Kick = 2
    PlayerInfo = 3
    SyncPlayer = 4
    SyncEquipment = 5
    RequestWorldData = 6
    WorldData = 7
    SpawnTileData = 8
    StatusTextSize = 9
    TileSection = 10
    # Deprecated. Framing happens as needed after TileSection is sent.
    TileFrameSection = 11
    PlayerSpawn = 12
    PlayerControls = 13
    PlayerActive = 14
    # Deprecated.
    Unknown15 = 15
    PlayerLifeMana = 16
```

With `Sets`, generates a separate class with `SetFactory`.

## 🛠 Development

- **Generator Version:** `1.1.0`
- **Author:** [Maksim Stashkevich](https://github.com/makstashkevich)
- **Terraria Version:** Auto-detected from `terrex.terrex.TERRARIA_VERSION`
- **CS Sources:** Decompile Terraria.exe using [dnSpy](https://github.com/dnSpy/dnSpy) or similar.

Changes to parser? Update `CsToPyParser`.

## 📄 License

[MIT](LICENSE.txt)

## 🙌 Contributing

Forks, PRs, issues welcome! Improve parser for new Terraria versions.

---
*Created with ❤️ for Terrex by Maksim Stashkevich*
