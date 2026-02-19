import re
from collections import defaultdict
from pathlib import Path
import traceback
from typing import Dict, List, Tuple

CS_FILE = Path(__file__).parent / '../terrex/world/MapHelper.cs'


def generate_color_code(cs_content: str, code_lines: List[str]):
    # color[287][0] = new Color(79, 128, 17);
    # colorArray2[158][0] = new Color(107, 49, 154);
    set_color_to_list_pattern = re.compile(
        r'color(\w+)?\s*\[\s*(\w+)\s*\]\s*\[\s*(\w+)\s*\]\s*=\s*new\s*Color\s*\(\s*(?:\(byte\))?\s*(\d+)\s*,\s*(?:\(byte\))?\s*(\d+)\s*,\s*(?:\(byte\))?\s*(\d+)(?:\s*,\s*(?:\(byte\))?\s*\d+)?\s*\)',
        re.MULTILINE | re.DOTALL,
    )

    # color[275][0] = color1;
    # colorArray2[1][0] = color1;
    set_ref_list_pattern = re.compile(r'color(\w+)?\[\s*(\d+)\s*\]\[\s*(\d+)\s*\]\s*=\s*(\w+)\s*;')

    # color[628][0] = color[627][1]
    # color[628][j] = color[627][j]
    set_ref_var_pattern = re.compile(r'color\s*\[\s*(\w+)\s*\]\s*\[\s*(\w+)\s*\]\s*=\s*color\s*\[\s*(\w+)\s*\]\s*\[\s*(\w+)\s*\]\s*;', re.MULTILINE)

    # for (int j = 0; j < (int)color[628].Length; j++)
    loop_var_len_pattern = re.compile(r'for\s*\(\s*int\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<\s*\(int\)\s*color\[(\d+)\]\.Length\s*;\s*\1\+\+\s*\)')

    # color1 = new Color(122, 217, 232);
    set_color_to_var_pattern = re.compile(r'(\w+)\s*=\s*new\s*Color\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*;')

    # color1 = color[53][0];
    set_var_to_var_pattern = re.compile(r'(\w+)\s*=\s*color\[\s*(\d+)\s*\]\[\s*(\d+)\s*\]\s*;')

    # colorArray = color[650];
    set_list_to_var_pattern = re.compile(r'(\w+)\s*=\s*color\[\s*(\d+)\s*\]\s*;')

    # for (int p = 0; p < (int)colorArray.Length; p++)
    loop_list_len_pattern = re.compile(r'for\s*\(\s*int\s+(\w+)\s*=\s*0\s*;\s*\1\s*<\s*\(int\)\s*(\w+)\.Length\s*;\s*\1\+\+\s*\)')

    # for (int s = 0; s < 13; s++)
    loop_int_pattern = re.compile(r'for\s*\(\s*int\s+(\w+)\s*=\s*\d+\s*;\s*\1\s*<\s*(\d+)\s*;.*\)')

    # for (int i = 0; i < TileID.Count; i++)
    loop_class_count_pattern = re.compile(r'for\s*\(\s*int\s+(\w+)\s*=\s*0\s*;\s*\1\s*<\s*(\w+)\.Count\s*;\s*\1\+\+\s*\)')

    # colorArray[o] = color[186][o];
    set_var_to_color_array_pattern = re.compile(r'(\w+)\s*\[\s*(\w+)\s*\]\s*=\s*(\w+)\s*\[\s*(\w+)\s*\]\s*\[\s*(\w+)\s*\]\s*;')

    # Color[] colorArray = color[647];
    array_assign_pattern = re.compile(r'(\w+\[\])\s+(\w+)\s*=\s*(\w+)\s*\[\s*(\d+)\s*\]\s*;')

    # Color color3 = new Color(250, 100, 50);
    color_assign_pattern = re.compile(r'Color\s+(\w+)\s*=\s*new\s*Color\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*;')

    # color[751][0] = Color.get_Gray();
    color_method_pattern = re.compile(r'(\w+)\s*\[\s*(\d+)\s*\]\[\s*(\d+)\s*\]\s*=\s*(\w+\.\w+\(\s*\))\s*;')

    # color[749][0] = color[138][0] * 0.95f;
    mul_pattern = re.compile(r'(\w+)\s*\[\s*(\d+)\s*\]\[\s*(\d+)\s*\]\s*=\s*' r'(\w+)\s*\[\s*(\d+)\s*\]\[\s*(\d+)\s*\]\s*\*\s*([0-9.]+)f\s*;')

    # Color[][] color = new Color[TileID.Count][];
    # Color[][] colorArray2 = new Color[WallID.Count][];
    wall_color_array_pattern = re.compile(r'Color\[\]\[\]\s+(\w+)\s*=\s*new\s+Color\[\s*(\w+)\.Count\s*\]\[\];')

    # color[i] = new Color[13];
    color_i_new_color = re.compile(r'(\w+)\[(\w+)\]\s*=\s*new\s*Color\[(\d+)\]')

    # -----
    # Color[] colorArray1 = new Color[] { new Color(9, 61, 191), new Color(253, 32, 3), new Color(254, 194, 20), new Color(161, 127, 255) };
    # -----
    # for all array
    array_pattern = re.compile(r'Color\[\]\s+(\w+)\s*=\s*new\s+Color\[\]\s*\{\s*(.*?)\s*\};')
    # only for color in array
    color_pattern = re.compile(r'new\s+Color\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)')

    lines = cs_content.splitlines()
    in_init = False
    is_loop = False

    for line in lines:
        line_clean = re.sub(r'^\s*//.*', '', line).strip()
        line_stripped = line_clean
        if 'public static void Initialize()' in line_clean:
            # print('init')
            in_init = True
            continue
        if '}' in line_clean and is_loop:
            # print('clean is_loop = false')
            is_loop = False
            continue
        if in_init and line_stripped == 'float single = 0.5f;':
            code_lines.append(
                """
    single = 0.5
    colorArray2[351][0] = color[734][0] * single
    colorArray2[352][0] = color[735][0] * single
    colorArray2[353][0] = color[170][0] * single
    colorArray2[354][0] = color[736][0] * single
    colorArray2[355][0] = color[737][0] * single
    colorArray2[356][0] = color[738][0] * single
    colorArray2[357][0] = color[739][0] * single
    colorArray2[358][0] = color[741][0] * single
    colorArray2[359][0] = color[742][0] * single
    colorArray2[360][0] = Color(73, 93, 116)
    colorArray2[361][0] = color[744][0] * single
    colorArray2[362][0] = color[745][0] * single
    colorArray2[363][0] = color[746][0] * single
    colorArray2[364][0] = color[747][0] * single
    colorArray2[365][0] = color[748][0] * single
    colorArray2[366][0] = color[749][0] * single

    colorArray3 = [Color()] * 256
    color6 = Color(50, 40, 255)
    color7 = Color(145, 185, 255)
    for u in range(len(colorArray3)):
        length = u / len(colorArray3)
        single1 = 1.0 - length
        colorArray3[u] = Color(
            int(color6.get_R() * single1 + color7.get_R() * length),
            int(color6.get_G() * single1 + color7.get_G() * length),
            int(color6.get_B() * single1 + color7.get_B() * length)
        )

    colorArray4 = [Color()] * 256
    color8 = Color(88, 61, 46)
    color9 = Color(37, 78, 123)
    for v in range(len(colorArray4)):
        single2 = v / 255
        single3 = 1.0 - single2
        colorArray4[v] = Color(
            int(color8.get_R() * single3 + color9.get_R() * single2),
            int(color8.get_G() * single3 + color9.get_G() * single2),
            int(color8.get_B() * single3 + color9.get_B() * single2)
        )

    colorArray5 = [Color()] * 256
    color10 = Color(74, 67, 60)
    color9 = Color(53, 70, 97)
    for w in range(len(colorArray5)):
        single4 = w / 255
        single5 = 1.0 - single4
        colorArray5[w] = Color(
            int(color10.get_R() * single5 + color9.get_R() * single4),
            int(color10.get_G() * single5 + color9.get_G() * single4),
            int(color10.get_B() * single5 + color9.get_B() * single4)
        )

    color11 = Color(50, 44, 38)
    num = 0
    MapHelper.tile_option_counts = [0] * TileID.Count
    for x in range(TileID.Count):
        colorArray6 = color[x]
        num1 = 0
        while num1 < 13 and colorArray6[num1] != Color.get_Transparent():
            num1 += 1
        MapHelper.tile_option_counts[x] = num1
        num += num1

    MapHelper.wall_option_counts = [0] * WallID.Count
    for y in range(WallID.Count):
        colorArray7 = colorArray2[y]
        num2 = 0
        while num2 < 2 and colorArray7[num2] != Color.get_Transparent():
            num2 += 1
        MapHelper.wall_option_counts[y] = num2
        num += num2

    num += 774
    MapHelper.color_lookup = [Color()] * num
    MapHelper.color_lookup[0] = Color.get_Transparent()
    num3 = 1
    MapHelper.tile_position = num3
    MapHelper.tile_lookup = [0] * TileID.Count

    for a in range(TileID.Count):
        if MapHelper.tile_option_counts[a] <= 0:
            MapHelper.tile_lookup[a] = 0
        else:
            # colorArray8 = color[a]
            MapHelper.tile_lookup[a] = num3
            for b in range(MapHelper.tile_option_counts[a]):
                MapHelper.color_lookup[num3] = color[a][b]
                num3 += 1

    MapHelper.wall_position = num3
    MapHelper.wall_lookup = [0] * WallID.Count
    MapHelper.wall_range_start = num3

    for c in range(WallID.Count):
        if MapHelper.wall_option_counts[c] <= 0:
            MapHelper.tile_lookup[c] = 0
        else:
            # colorArray9 = colorArray2[c]
            MapHelper.tile_lookup[c] = num3
            for d in range(MapHelper.wall_option_counts[c]):
                MapHelper.color_lookup[num3] = colorArray2[c][d]
                num3 += 1

    MapHelper.wall_range_end = num3
    MapHelper.liquid_position = num3
    for e in range(4):
        MapHelper.color_lookup[num3] = colorArray1[e]
        num3 += 1

    MapHelper.sky_position = num3
    for f in range(256):
        MapHelper.color_lookup[num3] = colorArray3[f]
        num3 += 1

    MapHelper.dirt_position = num3
    for g in range(256):
        MapHelper.color_lookup[num3] = colorArray4[g]
        num3 += 1

    MapHelper.rock_position = num3
    for h in range(256):
        MapHelper.color_lookup[num3] = colorArray5[h]
        num3 += 1

    MapHelper.hell_position = num3
    MapHelper.color_lookup[num3] = color11
    MapHelper.snow_types = [
        MapHelper.tile_lookup[147], MapHelper.tile_lookup[161], MapHelper.tile_lookup[162],
        MapHelper.tile_lookup[163], MapHelper.tile_lookup[164], MapHelper.tile_lookup[200]
    ]
"""
            )
            # print('stop')
            break
        if not in_init:
            continue

        # print(f'line={line_clean}')
        # print(f'is_loop={is_loop}')
        spacer = "    " * (2 if is_loop else 1)

        m = loop_var_len_pattern.search(line_clean)
        if m:
            var, start, tile = m.groups()
            code_lines.append(f"{spacer}for {var} in range({start}, len(color[{tile}])):")
            is_loop = True
            continue
        m = loop_class_count_pattern.search(line_clean)
        if m:
            var, length_source = m.groups()
            code_lines.append(f"{spacer}for {var} in range({length_source}.Count):")
            is_loop = True
            continue
        m = loop_int_pattern.search(line_clean)
        if m:
            var_name, end_val = m.groups()
            code_lines.append(f"{spacer}for {var_name} in range({end_val}):")
            is_loop = True
            continue
        m = loop_list_len_pattern.search(line_clean)
        if m:
            counter, array_name = m.groups()
            code_lines.append(f"{spacer}for {counter} in range(len({array_name})):")
            is_loop = True
            continue
        m = array_pattern.search(line_clean)
        if m:
            array_name, colors_str = m.groups()
            colors = color_pattern.findall(colors_str)
            colors = [tuple(map(int, c)) for c in colors]
            color_strs = [f"Color({r}, {g}, {b})" for r, g, b in colors]
            code_lines.append(f"{spacer}{array_name} = [{', '.join(color_strs)}]")
            continue
        m = set_var_to_color_array_pattern.search(line_clean)
        if m:
            target_array, target_index, source_array, source_index1, source_index2 = m.groups()
            code_lines.append(f"{spacer}{target_array}[{target_index}] = {source_array}[{source_index1}][{source_index2}]")
            continue
        m = wall_color_array_pattern.match(line_clean)
        if m:
            array_name, length_source = m.groups()
            code_lines.append(f"{spacer}{array_name} = [[] for _ in range({length_source}.Count)]")
            continue
        m = array_assign_pattern.match(line_clean)
        if m:
            vvar_type, var_name, source_array, source_index = m.groups()
            code_lines.append(f"{spacer}{var_name} = {source_array}[{source_index}]")
            continue
        m = color_assign_pattern.match(line_clean)
        if m:
            var_name, r, g, b = m.groups()
            code_lines.append(f"{spacer}{var_name} = Color({r}, {g}, {b})")
            continue
        m = color_method_pattern.match(line_clean)
        if m:
            var_name, row_index, col_index, method_call = m.groups()
            code_lines.append(f"{spacer}{var_name}[{row_index}][{col_index}] = {method_call}")
            continue

        m = set_color_to_var_pattern.match(line_clean)
        if m:
            var_name, r, g, b = m.groups()
            code_lines.append(f"{spacer}{var_name} = Color({r}, {g}, {b})")
            continue
        m = set_var_to_var_pattern.match(line_clean)
        if m:
            var_name, tile, opt = m.groups()
            code_lines.append(f"{spacer}{var_name} = color[{tile}][{opt}]")
            continue
        m = set_list_to_var_pattern.match(line_clean)
        if m:
            var_name, tile = m.groups()
            code_lines.append(f"{spacer}{var_name} = color[{tile}]")
        m = set_color_to_list_pattern.search(line_clean)
        if m:
            postfix, tile, opt, r, g, b = m.groups()
            # if line_clean == 'colorArray2[158][0] = new Color(107, 49, 154);':
            #     break
            code_lines.append(f'{spacer}color{postfix if postfix else ''}[{tile}][{opt}] = Color({r}, {g}, {b})')
            continue
        m = set_ref_list_pattern.search(line_clean)
        if m:
            # if line_clean == 'colorArray2[1][0] = color1;':
            #     break
            postfix, tile, opt, var_name = m.groups()
            code_lines.append(f'{spacer}color{postfix if postfix else ''}[{tile}][{opt}] = {var_name}')
            continue
        m = set_ref_var_pattern.search(line_clean)
        if m:
            tile, opt, refTile, refOpt = map(str, m.groups())
            code_lines.append(f'{spacer}color[{tile}][{opt}] = color[{refTile}][{refOpt}]')
            continue
        m = mul_pattern.search(line_clean)
        if m:
            tgt, ti1, ti2, src, si1, si2, factor = m.groups()
            code_lines.append(f'{spacer}{tgt}[{ti1}][{ti2}] = {src}[{si1}][{si2}] * {factor}')
            continue
        m = color_i_new_color.search(line_clean)
        if m:
            array_name, index_var, size = m.groups()
            code_lines.append(f'{spacer}{array_name}[{index_var}] = [Color() for _ in range({size})]')
            continue


def main():
    try:
        with open(CS_FILE, 'r', encoding='utf-8') as f:
            cs_content = f.read()
        code_lines = [
            '"""Auto-generated map colors from the decoded code of the Terraria game"""',
            '',
            'from terrex.id import TileID, WallID',
            'from terrex.net.rgb import Rgb as Color',
            'from terrex.world.map_helper import MapHelper',
            '',
            'def add_colors(MapHelper: MapHelper):',
        ]
        generate_color_code(cs_content, code_lines)

        target_file = Path(__file__).parent.parent / 'terrex/world/map_colors.py'
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(code_lines))
        print('Success! Created `terrex/world/map_colors.py`.')
    except Exception as e:
        print(traceback.format_exc())
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
