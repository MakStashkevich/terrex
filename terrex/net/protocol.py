# https://terraria.wiki.gg/wiki/Desktop_version_history
PROTOCOLS: dict[tuple[int, ...], int] = {
    # not tested
    # --- 2011 ---
    # 1.0 unknown
    # 1.0.1 unknown
    # 1.0.2 unknown
    # 1.0.3 unknown
    # 1.0.4 unknown
    # 1.0.5 unknown
    # 1.0.6 unknown
    # 1.0.6.1 unknown
    # 1.1 unknown
    # 1.1.1 unknown
    # --- 2012 ---
    # 1.1.2 unknown
    # --- 2013 ---
    # 1.2 unknown
    # 1.2.0.1 unknown
    # 1.2.0.2 unknown
    # 1.2.0.3 unknown
    # 1.2.0.3.1 unknown
    # 1.2.1 unknown
    # 1.2.1.1 unknown
    # 1.2.1.2 unknown
    # 1.2.2 unknown
    # --- 2014 ---
    # 1.2.3 unknown
    # 1.2.3.1 unknown
    # 1.2.4 unknown
    # 1.2.4.1 unknown
    # --- 2015 ---
    # 1.3.0.1 unknown
    # 1.3.0.2 unknown
    # 1.3.0.3 unknown
    # 1.3.0.4 unknown
    # 1.3.0.5 unknown
    # 1.3.0.6 unknown
    # 1.3.0.7 unknown
    # 1.3.0.8 unknown
    # --- 2016 ---
    # 1.3.1 unknown
    # 1.3.1.1 unknown
    # 1.3.2 unknown
    # 1.3.2.1 unknown
    # 1.3.3 unknown
    # 1.3.3.1 unknown
    # 1.3.3.2 unknown
    # 1.3.3.3 unknown
    # 1.3.4 unknown
    # 1.3.4.1 unknown
    # 1.3.4.2 unknown
    # 1.3.4.3 unknown
    # 1.3.4.4 unknown
    # --- 2017 ---
    # 1.3.5 unknown
    # 1.3.5.1 unknown
    # 1.3.5.2 unknown
    # 1.3.5.3 unknown
    # --- 2020 ---
    # 1.4.0.1 unknown
    # 1.4.0.2 unknown
    # 1.4.0.3 unknown
    # 1.4.0.4 unknown
    # 1.4.0.5 unknown
    #
    # --- 1.4.1.x ---
    #
    # 1.4.1.0 unknown
    # 1.4.1.1 unknown
    (1, 4, 1, 2): 234,  # 0xea00000001L
    #
    # --- 1.4.2.x ---
    # --- 2021 ---
    #
    # 1.4.2.0 unknown
    # 1.4.2.1 unknown
    # 1.4.2.2 unknown
    (1, 4, 2, 3): 238,  # 0xee00000001L
    #
    # --- 1.4.3.x ---
    #
    (1, 4, 3, 0): 242,  # 0xf200000001L
    (1, 4, 3, 1): 243,  # 0xf300000001L
    (1, 4, 3, 2): 244,  # 0xf400000001L
    # --- 2022 ---
    (1, 4, 3, 3): 245,  # 0xf500000001L (WorldGeneratorVersion)
    (1, 4, 3, 4): 246,  # 0xf600000001L
    (1, 4, 3, 5): 247,  # 0xf700000001L
    (1, 4, 3, 6): 248,  # 0xf800000001L
    #
    # --- 1.4.4.x ---
    #
    (1, 4, 4, 0): 269,  # 0x10d00000001L
    (1, 4, 4, 1): 270,  # 0x10e00000001L
    (1, 4, 4, 2): 271,  # 0x10f00000001L
    (1, 4, 4, 3): 272,  # 0x11000000001L
    (1, 4, 4, 4): 273,  # 0x11100000001L
    (1, 4, 4, 5): 274,  # 0x11200000001L
    (1, 4, 4, 6): 275,  # 0x11300000001L
    (1, 4, 4, 7): 276,  # 0x11400000001L
    (1, 4, 4, 8): 277,  # 0x11500000001L
    (1, 4, 4, 8, 1): 278,  # 0x11600000001L
    (1, 4, 4, 9): 279,  # 0x11700000001L
    #
    # --- 1.4.5.x ---
    # --- 2023 -> 2026 ---
    #
    (1, 4, 5, 0): 315,  # 0x13b00000001L
    # --- 2026 ---
    (1, 4, 5, 1): 315,  # 0x13b00000001L
    (1, 4, 5, 2): 315,  # 0x13b00000001L
    # 100% working fine
    (1, 4, 5, 3): 316,  # 0x13c00000001L
    (1, 4, 5, 4): 317,  # 0x13d00000001L
    (1, 4, 5, 5): 318,  # 0x13e00000001L
}
"""Terraria protocols by assembly version number. The key is the version tuple (major, minor, build, revision), the value is the protocol number."""
