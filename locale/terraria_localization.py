#!/usr/bin/env python3
"""
Terraria Localization Dumper.
Extracts JSON localization from exe into pretty JSON files.

Usage:
python terraria_localization.py <exe_path> <output_dir> <dump_all> [lang1 lang2 ...]

Examples:
- python terraria_localization.py /path/to/Terraria.exe locale/ false ru-RU en-US  # only specified
- python terraria_localization.py /path/to/Terraria.exe locale/ true               # all languages
"""

import json
import sys
import re
from pathlib import Path
from typing import List

try:
    from dnfile import dnPE
except ImportError:
    print("Install dnfile: pip install dnfile", file=sys.stderr)
    sys.exit(1)


def fix_json(text: str) -> str:
    """Fix common JSON issues like trailing commas."""
    text = re.sub(r',\s*([}\]])', r'\1', text)
    return text


def dump_localization(exe_path: str, output_dir: str, dump_all: bool, langs: List[str]):
    exe = Path(exe_path)
    if not exe.exists():
        print(f"File not found: {exe}", file=sys.stderr)
        sys.exit(1)

    asm = dnPE(str(exe))
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    dumped = 0
    net = asm.net
    resources_iter = net.resources if net is not None else []
    for resource in resources_iter:
        name_str = str(resource.name)
        if name_str.startswith("Terraria.Localization.Content"):
            parts = name_str.split('.')
            if len(parts) >= 4:
                res_lang = parts[3]
                if dump_all or res_lang in langs:
                    # Create lang dir
                    lang_dir = output_path / res_lang
                    lang_dir.mkdir(exist_ok=True)

                    # Filename: full from parts[3:]
                    res_filename = '.'.join(parts[3:])
                    res_path = lang_dir / res_filename

                    # Parse data as JSON
                    data = resource.data
                    if data is None or not isinstance(data, bytes):
                        continue
                    raw_data = data
                    if raw_data.startswith(b'\xef\xbb\xbf'):  # Skip BOM
                        raw_data = raw_data[3:]
                    text = raw_data.decode('utf-8')
                    text = fix_json(text)
                    data = json.loads(text)

                    # Pretty dump
                    with open(res_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)

                    print(f"Dumped: {res_path}")
                    dumped += 1

    if dumped == 0:
        print(f"No resources found (langs={langs}, dump_all={dump_all})", file=sys.stderr)
    else:
        print(f"Dumped {dumped} files to {output_path}")


def main():
    if len(sys.argv) < 4:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    exe_path = sys.argv[1]
    output_dir = sys.argv[2]
    dump_all_str = sys.argv[3].lower()
    dump_all = dump_all_str == 'true'
    langs = sys.argv[4:]  # optional langs at end

    dump_localization(exe_path, output_dir, dump_all, langs)


if __name__ == '__main__':
    main()
