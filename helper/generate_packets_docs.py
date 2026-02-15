import inspect
import re
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, '.')

from terrex.packets import packet_registry
from terrex.packets.base import ClientPacket, ServerPacket, SyncPacket
from terrex.structures.id import MessageID

size_map = {
    'byte': '1',
    'sbyte': '1',
    'short': '2',
    'ushort': '2',
    'int': '4',
    'single': '4',
    'float': '4',
    'double': '8',
    'ulong': '8',
    'string': '?',
    'dotnet_string': '?',
    'bool': '1',
}

canonical_types = {
    'byte': 'uint8',
    'sbyte': 'int8',
    'short': 'int16',
    'ushort': 'uint16',
    'int': 'int32',
    'ulong': 'uint64',
    'single': 'float32',
    'float': 'float32',
    'double': 'float64',
    'bool': 'bool',
    'string': 'string',
    'dotnet_string': 'string',
}


def get_direction(packet_cls):
    if issubclass(packet_cls, ClientPacket):
        return 'Client -> Server'
    elif issubclass(packet_cls, ServerPacket):
        return 'Server -> Client'
    else:
        return 'Server <-> Client (Sync)'


md = """# Packets structure for the Terraria multiplayer game

All packages described here are implemented in Terrex through reverse engineering and proxy and are relevant for the latest version of Terraria.

The package names and their data types are as close as possible to the original ones. 

**Attention!** If you find outdated packages, let I know by [making a new general discussion](https://github.com/MakStashkevich/terrex/discussions/new?category=general) with label "bug" or email me personally on [makstashkevich@gmail.com](mailto:makstashkevich@gmail.com?subject=Terrex%20Bug%20Report&body=Please%20describe%20the%20issue)

"""
md += '\n'

version_ranges = [
    (141, 161, "1.4.5.x"),
]
current_version = None

message_ids = sorted([m.value for m in MessageID])
for pid in message_ids:
    for start, end, ver in version_ranges:
        if start <= pid <= end:
            if current_version != ver:
                md += textwrap.dedent(f"""
<div align="center">
<h1>[ i ] Packets {start}-{end} have been added on versions {ver}</h1>
</div>

""")
                current_version = ver
            break
        
    if pid not in packet_registry:
        msg_id = MessageID(pid)
        cls_name = msg_id.name
        md += textwrap.dedent(f"""## {cls_name} [{pid}]
### Unknown Direction

> {'The packet has not been implemented yet.' if pid > 0 else 'It will never be implemented.'}
""")
        continue
    
    cls = packet_registry[pid]
    dir_str = get_direction(cls)

    packet_doc = cls.__doc__ if cls.__doc__ else None

    # Parse read method source for fields
    try:
        source = inspect.getsource(cls.read)
    except OSError:
        table = ''
    else:
        fields = []
        
        # Hardcoded fields for packets
        if pid == 1:
            fields.append("| ? | Version | string | 'Terraria123' where 123 is protocol version number |")
        elif pid == 10:
            fields.append("| ? | Compressed | raw deflate | Contains the following fields after decompression |")
            fields.append("| 4 | x_start | int32 | - |")
            fields.append("| 4 | y_start | int32 | - |")
            fields.append("| 2 | width | int16 | - |")
            fields.append("| 2 | height | int16 | - |")
            fields.append("| ? | tiles | Tile[y][x] | - |")
            fields.append("| ? | chests | Chest[] | - |")
            fields.append("| ? | signs | Sign[] | - |")
            fields.append("| ? | tile_entities | TileEntity[] | - |")
        else:
            for line in source.splitlines():
                # Match self.field = reader.read_type(
                m = re.match(r'\s*self\.(\w+)\s*=\s*reader\.(read_)?(\w+)\s*\([^)]*\)', line)
                if m:
                    field, prefix, rtype = m.groups()
                    size = size_map.get(rtype, '?')
                    typ = canonical_types.get(rtype, rtype)
                    fields.append(f"| {size} | {field} | {typ} | - |")
                # Match self.field = Vec2.read(reader)
                m2 = re.match(r'\s*self\.(\w+)\s*=\s*(\w+)\.read\s*\([^)]*\)', line)
                if m2:
                    field, struct = m2.groups()
                    size = '8'  # Vec2 2*single
                    typ = f'{struct}.read()'
                    fields.append(f"| {size} | {field} | {typ} | - |")

        if fields:
            table = '| Size (bytes) | Description | Type | Notes |\n| --- | --- | --- | --- |\n' + '\n'.join(fields) + '\n'
        else:
            table = '> This packet not contains any data.'

    module_path = cls.__module__.replace(".", "/")
    file_path = f"../{module_path}.py"
    md += f"## [{cls.__name__}]({file_path}) [{pid}]\n\n### {dir_str}{f'\n\n{packet_doc}' if packet_doc else ''}\n\n{table}\n\n"

print(md)

# Save to file
with open('docs/packets.md', 'w') as f:
    f.write(md)

print("Generated docs/packets.md")
