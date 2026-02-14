import os
import re
import ast
from pathlib import Path

PACKETS_DIR = Path(__file__).parent.parent / 'terrex/packets'
INIT_FILE = PACKETS_DIR / '__init__.py'

def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def get_main_class_name(file_path):
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read(), filename=str(file_path))
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, (ast.Name, ast.Attribute)):
                    base_name = base.id if isinstance(base, ast.Name) else base.attr
                    if base_name in ['ClientPacket', 'ServerPacket', 'SyncPacket', 'Packet']:
                        return node.name
    return None

def main():
    files_to_rename = []
    for file_path in PACKETS_DIR.glob('*.py'):
        if file_path.name in ['__init__.py', 'packet_ids.py', 'base.py']:
            continue
        class_name = get_main_class_name(file_path)
        if class_name:
            new_stem = camel_to_snake(class_name)
            new_path = file_path.parent / f'{new_stem}.py'
            if new_path != file_path:
                files_to_rename.append((file_path, new_path))
    
    for old_path, new_path in files_to_rename:
        os.rename(old_path, new_path)
        print(f'Переименован {old_path.name} -> {new_path.name}')
    
    print('Переименование файлов завершено.')

if __name__ == '__main__':
    main()
