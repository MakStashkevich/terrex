import re
from typing import List, Dict, Optional
import sys
from pathlib import Path


from enum import StrEnum


class TerrariaPath(StrEnum):
    ID = "Terraria.ID"


PATH_MAPPING: Dict[TerrariaPath, str] = {TerrariaPath.ID: "terrex/structures/id"}

ALLOWED_CLASSES: Dict[TerrariaPath, List[str]] = {
    TerrariaPath.ID: [
        "AchievementHelperID",
        "AmmoID",
        "AnimationID",
        "ArmorIDs",
        "BiomeConversionID",
        "BuffID",
        "DustID",
        "ExtrasID",
        "GameEventClearedID",
        "GameModeID",
        "GameVersionID",
        "GlowMaskID",
        "GoreID",
        "HousingCategoryID",
        "InvasionID",
        "ItemAlternativeFunctionID",
        "ItemHoldStyleID",
        "ItemID",
        "ItemSourceID",
        "ItemUseStyleID",
        "LiquidID",
        "MessageID",
        "MountID",
        "MusicID",
        "NPCHeadID",
        "NPCID",
        "PaintCoatingID",
        "PaintID",
        "PlayerDifficultyID",
        "PlayerTeamID",
        "PlayerTextureID",
        "PlayerVariantID",
        "PlayerVoiceID",
        "PlayerVoiceOverrideID",
        "PrefixID",
        "ProjectileDrawLayerID",
        "ProjectileID",
        "ProjectileSourceID",
        "StatusID",
        "SurfaceBackgroundID",
        "TeleportationSide",
        "TeleportationStyleID",
        "TileChangeType",
        "TileID",
        "TorchID",
        "TreeTopID",
        "WallID",
        "WaterStyleID",
    ]
}




class CsToPyParser:
    def __init__(self):
        self.lines: List[str] = []
        self.current_class = ""
        self.top_class: Optional[str] = None
        self.classes: Dict[str, Dict[str, str]] = {}
        self.class_stack: List[str] = []
        self.current_constants: Dict[str, str] = {}
        self.constants: Dict[str, str] = {}
        self.sets: Dict[str, str] = {}
        self.count_value: Optional[int] = None
        self.class_counts: Dict[str, int] = {}
        self.factory_size_var = None
        self.namespace = None
        self.pending_obsolete = False
        self.current_removed_constants: Dict[str, str] = {}
        self.removed_classes: Dict[str, Dict[str, str]] = {}
        self.pending_old_comment: Optional[str] = None
        self.current_old_comments: Dict[str, str] = {}
        self.old_comments_classes: Dict[str, Dict[str, str]] = {}
        self.is_enum = False

    def parse(self, content: str) -> str:
        self.lines = content.splitlines()
        self._reset()

        i = 0
        while i < len(self.lines):
            line_raw = self.lines[i]
            indent = len(line_raw) - len(line_raw.lstrip())
            stripped = line_raw.strip()
            line = stripped

            if line.startswith("namespace "):
                m = re.match(r"namespace\s+([^\s{;]+)", line)
                if m:
                    self.namespace = m.group(1)

            m_enum = re.match(r"(?:public|internal)\s+enum\s+(\S+)", stripped)
            if m_enum:
                class_name = m_enum.group(1).rstrip("{").strip()
                if self.top_class is None:
                    self.top_class = class_name
                self.is_enum = True
                i += 1
                continue

            m_class = re.match(r"(?:public|internal)(?:\s+static)?\s+class\s+(\S+)", stripped)
            if m_class:
                class_name = m_class.group(1).rstrip("{").strip()
                if self.top_class is None:
                    self.top_class = class_name
                if class_name != "Sets":
                    self.class_stack.append((class_name, indent))
                    i += 1
                    continue
                # For Sets, continue parsing inner lines without skipping

            if self.is_enum:
                m_member = re.match(r"^(\w+)\s*(=\s*(\d+))?\s*,?\s*$", stripped)
                if m_member:
                    name = m_member.group(1)
                    val = str(len(self.current_constants))
                    self.current_constants[name] = val
                    i += 1
                    continue

            if re.match(r"^\[Obsolete\(\"Removed\",\s*true\)\]$", stripped):
                self.pending_obsolete = True
                i += 1
                continue

            m_old = re.match(r"^\[Old\(\"([^\"]+)\"\)\]$", stripped)
            if m_old:
                self.pending_old_comment = m_old.group(1)
                i += 1
                continue

            # константы
            m_const = re.match(r"public const (?:int|ushort|byte|short|sbyte) (\w+)\s*=\s*([^;]+);", line)
            if m_const:
                name, val = m_const.groups()
                val = val.strip()
                if self.pending_obsolete:
                    self.current_removed_constants[name] = val
                    self.pending_obsolete = False
                else:
                    self.current_constants[name] = val
                    if self.pending_old_comment:
                        self.current_old_comments[name] = self.pending_old_comment
                        self.pending_old_comment = None
                if name == "Count":
                    self.count_value = int(val)
                i += 1
                continue

            # fallback for readonly Count
            if re.match(r"public readonly static .*?Count;", line) or "Count =" in line:
                m_val = re.search(r"Count\s*=\s*(\d+)", line)
                if m_val:
                    self.count_value = int(m_val.group(1))
                else:
                    j = i + 1
                    while j < len(self.lines):
                        if "Count =" in self.lines[j]:
                            m_val = re.search(r"Count\s*=\s*(\d+)", self.lines[j])
                            if m_val:
                                self.count_value = int(m_val.group(1))
                                break
                        j += 1
                i += 1
                continue

            # static ctor assignments
            m_assign = re.match(r"(\w+)\.(\w+)\s*=\s*(\d+);", stripped)
            if m_assign:
                class_ref, name, val = m_assign.groups()
                if class_ref == self.top_class:
                    self.current_constants[name] = val
                    if name == "Count":
                        self.count_value = int(val)
                i += 1
                continue

            if stripped == "}":
                if self.is_enum and not self.class_stack:
                    self.classes[self.top_class] = self.current_constants.copy()
                    self.is_enum = False
                    self.current_constants.clear()
                    self.current_removed_constants.clear()
                    self.current_old_comments.clear()
                    i += 1
                    continue
                if self.class_stack and indent == self.class_stack[-1][1]:
                    popped_name, _ = self.class_stack.pop()
                    current_path = '.'.join(name for name, _ in self.class_stack) + ('.' + popped_name if self.class_stack else popped_name)
                    self.classes[current_path] = self.current_constants.copy()
                    self.removed_classes[current_path] = self.current_removed_constants.copy()
                    self.old_comments_classes[current_path] = self.current_old_comments.copy()
                    self.current_old_comments.clear()
                    self.current_removed_constants.clear()
                    if self.count_value is not None:
                        self.class_counts[current_path] = self.count_value
                    self.current_constants.clear()
                    self.count_value = None
                i += 1
                continue



            # SetFactory
            if ".Factory = new SetFactory(" in line:
                m = re.search(r"new SetFactory\(([^)]+)\)", line)
                if m:
                    self.factory_size_var = m.group(1).strip()
                i += 1
                continue

            # Factory CreateSet
            if ".Factory.Create" in line:
                parts = re.split(r"\s*=\s*", line.strip(), maxsplit=1)
                if len(parts) == 2:
                    left = parts[0].strip()
                    right = parts[1].strip()
                    m_create = re.search(
                        r"Factory\.Create([A-Z][a-z]+)Set\s*\(\s*([^)]+)\)\s*", right
                    )
                    if m_create:
                        set_type = m_create.group(1)
                        args_str = m_create.group(2)
                        set_name = left.rsplit(".", 1)[-1]
                        py_set = self._convert_set_call(set_type, args_str)
                        if py_set:
                            self.sets[set_name] = py_set
                i += 1
                continue

            # new int[] or bool[]
            if "new int[]" in line or "new bool[]" in line:
                parts = re.split(r"\s*=\s*", line.strip(), maxsplit=1)
                if len(parts) == 2:
                    left = parts[0].strip()
                    right = parts[1].strip()
                    m_array = re.search(r"new\s+(int|bool)\[\]\s*\{([^}]+)\}", right)
                    if m_array:
                        arr_type = m_array.group(1)
                        content = m_array.group(2).strip()
                        set_name = left.rsplit(".", 1)[-1]
                        content = re.sub(r"\s*,\s*", ",", content)
                        vals = [v.strip() for v in content.split(",") if v.strip()]
                        if arr_type == "int":
                            self.sets[set_name] = "[" + ", ".join(vals) + "]"
                        elif arr_type == "bool":
                            py_vals = [
                                (
                                    "True"
                                    if v.lower().strip() == "true"
                                    else "False" if v.lower().strip() == "false" else v
                                )
                                for v in vals
                            ]
                            self.sets[set_name] = "[" + ", ".join(py_vals) + "]"

                    
                i += 1
                continue

            i += 1



        # Validation
        if not self.namespace:
            raise ValueError("Namespace not found")
        supported = [e.value for e in TerrariaPath]
        if self.namespace not in supported:
            raise ValueError(
                f"Namespace '{self.namespace}' not supported. Supported: {', '.join(supported)}"
            )
        if not self.top_class:
            raise ValueError("Class not found")
        self.current_class = self.top_class
        if self.sets:
            if self.factory_size_var is None:
                raise ValueError("SetFactory initialization not found")

        return self._generate_python_code()

    def _reset(self):
        self.current_class = ""
        self.top_class = None
        self.classes = {}
        self.class_stack = []
        self.current_constants = {}
        self.constants = {}
        self.sets = {}
        self.count_value = None
        self.class_counts = {}
        self.factory_size_var = None
        self.namespace = None
        self.pending_obsolete = False
        self.current_removed_constants = {}
        self.removed_classes = {}
        self.pending_old_comment = None
        self.current_old_comments = {}
        self.old_comments_classes = {}
        self.is_enum = False

    def _convert_set_call(self, set_type: str, args_str: str) -> Optional[str]:
        # Remove new int[] {} if present
        args_str = re.sub(r"new\s+(int|bool)\[\]\s*\{", "", args_str)
        args_str = re.sub(r"new\s+(int|bool)\s*\[\s*0\s*\]", "", args_str)
        args_str = args_str.replace("}", "").strip()
        if not args_str:
            return None

        items = [x.strip() for x in args_str.split(",") if x.strip()]

        if set_type == "Bool":
            ids_list = items[:]
            default = False
            if ids_list and ids_list[0].lower() in ("true", "false"):
                default = ids_list[0].lower() == "true"
                ids_list = ids_list[1:]
            if ids_list:
                if all(item.isdigit() for item in ids_list):
                    py_args = ', '.join(ids_list)
                else:
                    py_args = '[' + ', '.join(ids_list) + ']'
                return f"factory.create_bool_set({default}, {py_args})"
            else:
                return f"factory.create_bool_set({default})"
        elif set_type == "Int":
            default = -1
            pairs = []
            if items and all(
                c.replace("-", "").isdigit() for c in items[:2] if items[:2]
            ):
                default = int(items[0])
                pairs = items[1:]
            else:
                pairs = []
                for item in items:
                    stripped_item = item.strip()
                    if stripped_item:
                        parts = stripped_item.split('.')
                        # accept ItemID.Name format constants - other skipped
                        if len(parts) == 2:
                            pairs.append(stripped_item)
            
            pairs_str = ", ".join(pairs)
            if not pairs_str:
                pairs_str = "0"
            return f"factory.create_int_set({default}, {pairs_str})"
        return None

    def _generate_python_code(self) -> str:
        out = [
            f"# {self.current_class} autogenerated from {self.namespace}",
            "",
        ]
        is_pure_enum = lambda consts: consts and all(val.lstrip('-').isdigit() for val in consts.values())
        top_path = self.top_class
        top_consts = self.classes.get(top_path, {})
        top_is_pure = is_pure_enum(top_consts)
        max_count = max(self.class_counts.values()) if self.class_counts else 0
        has_sets = bool(self.sets)
        if has_sets:
            imports = [
                "from terrex.structures.id.set_factory import SetFactory",
                "from enum import IntEnum, auto"
            ]
            if self.factory_size_var != f"{self.current_class}.Count":
                ext_class = self.factory_size_var.rsplit(".", 1)[0]
                imports.append(f"from terrex.structures.id.{ext_class} import {ext_class}")
            out.extend(imports)
            out.append("")
            class_def = f"class {self.current_class}(IntEnum):" if top_is_pure else f"class {self.current_class}:"
            out.append(class_def)
            top_old_comments = self.old_comments_classes.get(top_path, {})
            top_removed = self.removed_classes.get(top_path, {})
            const_items = [(int(val), name, val, False) for name, val in top_consts.items() if val.lstrip('-').isdigit()]
            removed_items = [(int(val), name, val, True) for name, val in top_removed.items()]
            all_items = sorted(const_items + removed_items)
            for _, name, val, is_removed in all_items:
                if is_removed:
                    out.append(f"    # {name} = {val}")
                else:
                    old_comment = top_old_comments.get(name)
                    if old_comment:
                        out.append(f"    # {old_comment}")
                    out.append(f"    {name} = {val}")
            out.append(f"    Count = {max_count}")
        else:
            out.append("from enum import IntEnum, auto")
            out.append("")
            enum_type = "IntEnum" if is_pure_enum(top_consts) else "auto"
            out.append(f"class {self.current_class}({enum_type}):")
            top_old_comments = self.old_comments_classes.get(top_path, {})
            top_removed = self.removed_classes.get(top_path, {})
            const_items = [(int(val), name, val, False) for name, val in top_consts.items() if val.lstrip('-').isdigit()]
            removed_items = [(int(val), name, val, True) for name, val in top_removed.items()]
            all_items = sorted(const_items + removed_items)
            for _, name, val, is_removed in all_items:
                if is_removed:
                    out.append(f"    # {name} = {val}")
                else:
                    old_comment = top_old_comments.get(name)
                    if old_comment:
                        out.append(f"    # {old_comment}")
                    out.append(f"    {name} = {val}")
        out.append("")
        # sub classes
        sub_classes = [p for p in self.classes if p.startswith(self.top_class + '.')]
        for path in sorted(sub_classes, key=lambda p: p.split('.')[-1]):
            sub_name = path.split('.')[-1]
            consts = self.classes[path]
            enum_type = "IntEnum" if is_pure_enum(consts) else "auto"
            out.append(f"    class {sub_name}({enum_type}):")
            sub_old_comments = self.old_comments_classes.get(path, {})
            sub_removed = self.removed_classes.get(path, {})
            const_items = [(int(val), name, val, False) for name, val in consts.items() if val.lstrip('-').isdigit()]
            removed_items = [(int(val), name, val, True) for name, val in sub_removed.items()]
            all_items = sorted(const_items + removed_items)
            for _, name, val, is_removed in all_items:
                if is_removed:
                    out.append(f"        # {name} = {val}")
                else:
                    old_comment = sub_old_comments.get(name)
                    if old_comment:
                        out.append(f"        # {old_comment}")
                    out.append(f"        {name} = {val}")
            sub_count = self.class_counts.get(path)
            if sub_count is not None:
                out.append(f"        Count = {sub_count}")
            out.append("")
        if has_sets:
            out.append("")
            out.append(f"factory = SetFactory({self.factory_size_var})")
            out.append("")
            out.append("")
            out.append(f"class {self.current_class}Sets:")
            for name, code in sorted(self.sets.items()):
                out.append(f"    {name} = {code}")
            out.append("")
        return "\n".join(out)


def find_cs_files(folder: Path, max_depth: int = 3) -> list[Path]:
    cs_paths = []
    def walk(p: Path, depth: int):
        if depth > max_depth:
            return
        try:
            for child in p.iterdir():
                if child.is_file() and child.suffix == ".cs":
                    cs_paths.append(child)
                elif child.is_dir():
                    walk(child, depth + 1)
        except PermissionError:
            pass
    walk(folder, 0)
    return cs_paths

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Terraria C# to Python classes generator")
    parser.add_argument("path", help="Path to CS file or folder")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively find and generate all .cs files up to depth 3")
    args = parser.parse_args()

    cs_paths = []
    if args.recursive:
        folder = Path(args.path)
        if not folder.is_dir():
            print(f"Error: {args.path} is not a directory")
            sys.exit(1)
        cs_paths = find_cs_files(folder)
        if not cs_paths:
            print(f"No .cs files found in {args.path} up to depth 3")
            sys.exit(0)
    else:
        cs_path = Path(args.path)
        if not cs_path.exists():
            print(f"File not found: {cs_path}")
            sys.exit(1)
        if not str(cs_path).endswith(".cs"):
            print("Single mode requires .cs file")
            sys.exit(1)
        cs_paths = [cs_path]

    success_count = 0
    total = len(cs_paths)
    for cs_path in cs_paths:
        try:
            with open(cs_path, "r", encoding="utf-8") as f:
                content = f.read()
            parser_obj = CsToPyParser()
            python_result = parser_obj.parse(content)

            namespace_path = PATH_MAPPING[TerrariaPath(parser_obj.namespace)]
            class_name = parser_obj.current_class
            terraria_path = TerrariaPath(parser_obj.namespace)
            if terraria_path in ALLOWED_CLASSES and class_name not in ALLOWED_CLASSES[terraria_path]:
                print(f"Skipping {cs_path.name} ({class_name}.py) - not in allowed list for {terraria_path.value}")
                continue
            snake_name = class_name + ".py"
            output_dir = Path(namespace_path)
            output_path = output_dir / snake_name
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(python_result)
            print(f"Saved to {output_path}")
            success_count += 1
        except ValueError as e:
            print(f"Validation error in {cs_path.name}: {e}")
        except Exception as e:
            print(f"Parsing error in {cs_path.name}: {e}")

    print(f"Done: {success_count}/{total} successful")
