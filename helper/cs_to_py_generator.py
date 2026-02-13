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
        self.count_value: Optional[int] = None
        self.class_counts: Dict[str, int] = {}
        self.namespace = None
        self.pending_obsolete = False
        self.current_removed_constants: Dict[str, str] = {}
        self.removed_classes: Dict[str, Dict[str, str]] = {}
        self.pending_old_comment: Optional[str] = None
        self.current_old_comments: Dict[str, str] = {}
        self.old_comments_classes: Dict[str, Dict[str, str]] = {}
        self.is_enum = False
        self.sets_by_class: Dict[str, Dict[str, str]] = {}
        self.current_sets_owner: Optional[str] = None
        self.factory_count_ref: Dict[str, str] = {}

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
            if "Sets.Factory" in stripped and "new SetFactory" in stripped:
                m = re.search(r"(\w+(?:\.\w+)*)\.Sets\.Factory\s*=\s*new SetFactory\s*\(\s*([^)]+)\)", stripped)
                if m:
                    owner = m.group(1)
                    self.current_sets_owner = owner
                    m_count = re.search(r'(\w+(?:\.\w+)*)\.Count', m.group(2))
                    sub_name_key = owner.split('.')[-1]
                    self.factory_count_ref[sub_name_key] = m_count.group(1) if m_count else self.top_class
                i += 1
                continue

            # Factory CreateSet
            if ".Factory.Create" in line and self.current_sets_owner:
                # print(f"DEBUG entering Factory.Create block: line={repr(line)}, owner={repr(self.current_sets_owner)}")
                parts = re.split(r"\s*=\s*", line.strip(), maxsplit=1)
                if len(parts) == 2:
                    left = parts[0].strip()
                    set_name = left.rsplit('.', 1)[-1]
                    if set_name.__len__() > 1:
                        right = parts[1].strip()
                        m_create = re.search(
                            r"Factory.Create([A-Z][a-z]+)Set\s*\(\s*([^)]+)\)\s*", right
                        )
                        if m_create:
                            set_type = m_create.group(1)
                            args_str = m_create.group(2)
                            py_set = self._convert_set_call(set_type, args_str)
                            if py_set:
                                if self.current_sets_owner not in self.sets_by_class:
                                    self.sets_by_class[self.current_sets_owner] = {}
                                self.sets_by_class[self.current_sets_owner][set_name] = py_set
                                left_parts = [p.strip() for p in left.split(".")]
                                if len(left_parts) >= 4 and left_parts[0] == self.top_class and left_parts[1] == "Sets":
                                    sub_prefix = '.'.join(left_parts[2:-1])
                                    if sub_prefix:
                                        effective_owner = f"{self.current_sets_owner}.{sub_prefix}"
                                        if effective_owner not in self.sets_by_class:
                                            self.sets_by_class[effective_owner] = {}
                                        self.sets_by_class[effective_owner][set_name] = py_set
                i += 1
                continue

            # new int[] or bool[]
            if ("new int[]" in line or "new bool[]" in line) and self.current_sets_owner:
                parts = re.split(r"\s*=\s*", line.strip(), maxsplit=1)
                if len(parts) == 2:
                    left = parts[0].strip()
                    m_set = re.search(r".*\\.Sets\\.(\\w+)\\s*$", left)
                    if m_set:
                        set_name = m_set.group(1)
                        right = parts[1].strip()
                        m_array = re.search(r"new\s+(int|bool)\s*\[.*?\]\s*\{([^}]+)\}", right)
                        if m_array:
                            arr_type = m_array.group(1)
                            content = m_array.group(2).strip()
                            set_name = left.rsplit(".", 1)[-1]
                            content = re.sub(r"\s*,\s*", ",", content)
                            vals = [v.strip() for v in content.split(",") if v.strip()]
                            if self.current_sets_owner not in self.sets_by_class:
                                self.sets_by_class[self.current_sets_owner] = {}
                            if arr_type == "int":
                                py_code = "[" + ", ".join(vals) + "]"
                                self.sets_by_class[self.current_sets_owner][set_name] = py_code
                            elif arr_type == "bool":
                                py_vals = [
                                    (
                                        "True"
                                        if v.lower().strip() == "true"
                                        else "False" if v.lower().strip() == "false" else v
                                    )
                                    for v in vals
                                ]
                                py_code = "[" + ", ".join(py_vals) + "]"
                                self.sets_by_class[self.current_sets_owner][set_name] = py_code
                            left_parts = [p.strip() for p in left.split(".")]
                            if len(left_parts) >= 4 and left_parts[0] == self.top_class and left_parts[1] == "Sets":
                                sub_prefix = '.'.join(left_parts[2:-1])
                                if sub_prefix:
                                    effective_owner = f"{self.current_sets_owner}.{sub_prefix}"
                                    if effective_owner not in self.sets_by_class:
                                        self.sets_by_class[effective_owner] = {}
                                    self.sets_by_class[effective_owner][set_name] = py_code

                    
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


        # print("DEBUG PARSE END: sets_by_class =", repr(self.sets_by_class))
        # print("DEBUG PARSE END: current_sets_owner =", repr(self.current_sets_owner))
        # print("DEBUG PARSE END: class_counts =", repr(self.class_counts))
        return self._generate_python_code()

    def _reset(self):
        self.current_class = ""
        self.top_class = None
        self.classes = {}
        self.class_stack = []
        self.current_constants = {}
        self.constants = {}
        self.count_value = None
        self.class_counts = {}
        self.namespace = None
        self.pending_obsolete = False
        self.current_removed_constants = {}
        self.removed_classes = {}
        self.pending_old_comment = None
        self.current_old_comments = {}
        self.old_comments_classes = {}
        self.is_enum = False
        self.sets_by_class = {}
        self.current_sets_owner = None
        self.factory_count_ref = {}

    def _convert_set_call(self, set_type: str, args_str: str) -> Optional[str]:
        # print(f"DEBUG _convert_set_call ENTER: type='{set_type}', args_in='{repr(args_str)}'")
        # Remove new int[] {} if present
        args_str = re.sub(r"new\s+(int|bool)\s*\[.*?\]\s*\{", "", args_str)
        # print(f"DEBUG _convert after sub: '{repr(args_str)}'")
        args_str = re.sub(r"new\s+(int|bool)\s*\[\s*0\s*\]", "", args_str)
        args_str = args_str.replace("}", "").strip()
        # print(f"DEBUG _convert after clean: '{repr(args_str)}', items={[x.strip() for x in args_str.split(',') if x.strip()]}")
        if not args_str:
            # print("DEBUG _convert return None (empty)")
            return None
        # args_str = re.sub(r"new\s+(int|bool)\s*\[\s*0\s*\]", "", args_str)
        # args_str = args_str.replace("}", "").strip()
        # if not args_str:
        #     return None

        # Fix for new int[N] without {}
        if re.match(r'^\s*new\s+(int|bool)\s*\[\s*\d+\s*\]\s*', args_str):
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
        has_sets = bool(self.sets_by_class)
        if has_sets:
            imports = [
                "from terrex.structures.id.set_factory import SetFactory",
                "from enum import IntEnum, auto"
            ]

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
            sub_count = self.class_counts.get(path)
            sub_old_comments = self.old_comments_classes.get(path, {})
            sub_removed = self.removed_classes.get(path, {})
            if not consts and not sub_removed and not sub_old_comments and sub_count is None:
                continue
            enum_type = "IntEnum" if is_pure_enum(consts) else "auto"
            out.append(f"    class {sub_name}({enum_type}):")
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

        out.append("")

        sets_map = {}
        for owner_path, sets_dict in self.sets_by_class.items():
            sub_name_key = owner_path.split('.')[-1]
            sets_map[sub_name_key] = sets_dict
        if has_sets:
            out.append(f"class {self.current_class}Sets:")
            for sub_name in sorted(sets_map):
                parent_ref = self.factory_count_ref.get(sub_name, self.current_class)
                out.append(f"    class {sub_name}:")
                out.append(f"        factory = SetFactory({parent_ref}.Count)")
                for name, code in sorted(sets_map[sub_name].items()):
                    out.append(f"        {name} = {code}")
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
