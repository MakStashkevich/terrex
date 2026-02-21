from dataclasses import dataclass

from terrex.net.streamer import Reader, Writer


@dataclass
class Rgb:
    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 0

    def __init__(self, r: int | None = None, g: int | None = None, b: int | None = None, a: int | None = None) -> None:
        # new Color()
        if r is None and g is None and b is None and a is None:
            self.r = 0
            self.g = 0
            self.b = 0
            self.a = 0
            return

        # new Color(r,g,b)
        if r is not None and g is not None and b is not None and a is None:
            self.r = r
            self.g = g
            self.b = b
            self.a = 255
            return

        # new Color(r,g,b,a)
        if r is not None and g is not None and b is not None and a is not None:
            self.r = r
            self.g = g
            self.b = b
            self.a = a
            return

        raise ValueError("Invalid constructor arguments")

    def get_R(self) -> int:
        return self.r

    def get_G(self) -> int:
        return self.g

    def get_B(self) -> int:
        return self.b

    def get_A(self) -> int:
        return self.a

    @classmethod
    def get_Transparent(cls):
        return cls(0, 0, 0, 0)

    @classmethod
    def read(cls, reader: Reader) -> 'Rgb':
        return cls(
            reader.read_byte(),
            reader.read_byte(),
            reader.read_byte(),
        )

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.r)
        writer.write_byte(self.g)
        writer.write_byte(self.b)

    def __mul__(self, scalar: int | float) -> 'Rgb':
        return Rgb(int(self.r * scalar), int(self.g * scalar), int(self.b * scalar))

    def __str__(self):
        return f"Rgb(r={self.r}, g={self.g}, b={self.b}, a={self.a})"

    @classmethod
    def get_AliceBlue(cls) -> 'Rgb':
        return cls(240, 248, 255)

    @classmethod
    def get_AntiqueWhite(cls) -> 'Rgb':
        return cls(250, 235, 215)

    @classmethod
    def get_Aqua(cls) -> 'Rgb':
        return cls(0, 255, 255)

    @classmethod
    def get_Aquamarine(cls) -> 'Rgb':
        return cls(127, 255, 212)

    @classmethod
    def get_Azure(cls) -> 'Rgb':
        return cls(240, 255, 255)

    @classmethod
    def get_Beige(cls) -> 'Rgb':
        return cls(245, 245, 220)

    @classmethod
    def get_Bisque(cls) -> 'Rgb':
        return cls(255, 228, 196)

    @classmethod
    def get_Black(cls) -> 'Rgb':
        return cls(0, 0, 0)

    @classmethod
    def get_BlanchedAlmond(cls) -> 'Rgb':
        return cls(255, 235, 205)

    @classmethod
    def get_Blue(cls) -> 'Rgb':
        return cls(0, 0, 255)

    @classmethod
    def get_BlueViolet(cls) -> 'Rgb':
        return cls(138, 43, 226)

    @classmethod
    def get_Brown(cls) -> 'Rgb':
        return cls(165, 42, 42)

    @classmethod
    def get_BurlyWood(cls) -> 'Rgb':
        return cls(222, 184, 135)

    @classmethod
    def get_CadetBlue(cls) -> 'Rgb':
        return cls(95, 158, 160)

    @classmethod
    def get_Chartreuse(cls) -> 'Rgb':
        return cls(127, 255, 0)

    @classmethod
    def get_Chocolate(cls) -> 'Rgb':
        return cls(210, 105, 30)

    @classmethod
    def get_Coral(cls) -> 'Rgb':
        return cls(255, 127, 80)

    @classmethod
    def get_CornflowerBlue(cls) -> 'Rgb':
        return cls(100, 149, 237)

    @classmethod
    def get_Cornsilk(cls) -> 'Rgb':
        return cls(255, 248, 220)

    @classmethod
    def get_Crimson(cls) -> 'Rgb':
        return cls(220, 20, 60)

    @classmethod
    def get_Cyan(cls) -> 'Rgb':
        return cls(0, 255, 255)

    @classmethod
    def get_DarkBlue(cls) -> 'Rgb':
        return cls(0, 0, 139)

    @classmethod
    def get_DarkCyan(cls) -> 'Rgb':
        return cls(0, 139, 139)

    @classmethod
    def get_DarkGoldenrod(cls) -> 'Rgb':
        return cls(184, 134, 11)

    @classmethod
    def get_DarkGray(cls) -> 'Rgb':
        return cls(169, 169, 169)

    @classmethod
    def get_DarkGreen(cls) -> 'Rgb':
        return cls(0, 100, 0)

    @classmethod
    def get_DarkKhaki(cls) -> 'Rgb':
        return cls(189, 183, 107)

    @classmethod
    def get_DarkMagenta(cls) -> 'Rgb':
        return cls(139, 0, 139)

    @classmethod
    def get_DarkOliveGreen(cls) -> 'Rgb':
        return cls(85, 107, 47)

    @classmethod
    def get_DarkOrange(cls) -> 'Rgb':
        return cls(255, 140, 0)

    @classmethod
    def get_DarkOrchid(cls) -> 'Rgb':
        return cls(153, 50, 204)

    @classmethod
    def get_DarkRed(cls) -> 'Rgb':
        return cls(139, 0, 0)

    @classmethod
    def get_DarkSalmon(cls) -> 'Rgb':
        return cls(233, 150, 122)

    @classmethod
    def get_DarkSeaGreen(cls) -> 'Rgb':
        return cls(143, 188, 143)

    @classmethod
    def get_DarkSlateBlue(cls) -> 'Rgb':
        return cls(72, 61, 139)

    @classmethod
    def get_DarkSlateGray(cls) -> 'Rgb':
        return cls(47, 79, 79)

    @classmethod
    def get_DarkTurquoise(cls) -> 'Rgb':
        return cls(0, 206, 209)

    @classmethod
    def get_DarkViolet(cls) -> 'Rgb':
        return cls(148, 0, 211)

    @classmethod
    def get_DeepPink(cls) -> 'Rgb':
        return cls(255, 20, 147)

    @classmethod
    def get_DeepSkyBlue(cls) -> 'Rgb':
        return cls(0, 191, 255)

    @classmethod
    def get_DimGray(cls) -> 'Rgb':
        return cls(105, 105, 105)

    @classmethod
    def get_DodgerBlue(cls) -> 'Rgb':
        return cls(30, 144, 255)

    @classmethod
    def get_Firebrick(cls) -> 'Rgb':
        return cls(178, 34, 34)

    @classmethod
    def get_FloralWhite(cls) -> 'Rgb':
        return cls(255, 250, 240)

    @classmethod
    def get_ForestGreen(cls) -> 'Rgb':
        return cls(34, 139, 34)

    @classmethod
    def get_Fuchsia(cls) -> 'Rgb':
        return cls(255, 0, 255)

    @classmethod
    def get_Gainsboro(cls) -> 'Rgb':
        return cls(220, 220, 220)

    @classmethod
    def get_GhostWhite(cls) -> 'Rgb':
        return cls(248, 248, 255)

    @classmethod
    def get_Gold(cls) -> 'Rgb':
        return cls(255, 215, 0)

    @classmethod
    def get_Goldenrod(cls) -> 'Rgb':
        return cls(218, 165, 32)

    @classmethod
    def get_Gray(cls) -> 'Rgb':
        return cls(128, 128, 128)

    @classmethod
    def get_Green(cls) -> 'Rgb':
        return cls(0, 128, 0)

    @classmethod
    def get_GreenYellow(cls) -> 'Rgb':
        return cls(173, 255, 47)

    @classmethod
    def get_Honeydew(cls) -> 'Rgb':
        return cls(240, 255, 240)

    @classmethod
    def get_HotPink(cls) -> 'Rgb':
        return cls(255, 105, 180)

    @classmethod
    def get_IndianRed(cls) -> 'Rgb':
        return cls(205, 92, 92)

    @classmethod
    def get_Indigo(cls) -> 'Rgb':
        return cls(75, 0, 130)

    @classmethod
    def get_Ivory(cls) -> 'Rgb':
        return cls(255, 255, 240)

    @classmethod
    def get_Khaki(cls) -> 'Rgb':
        return cls(240, 230, 140)

    @classmethod
    def get_Lavender(cls) -> 'Rgb':
        return cls(230, 230, 250)

    @classmethod
    def get_LavenderBlush(cls) -> 'Rgb':
        return cls(255, 240, 245)

    @classmethod
    def get_LawnGreen(cls) -> 'Rgb':
        return cls(124, 252, 0)

    @classmethod
    def get_LemonChiffon(cls) -> 'Rgb':
        return cls(255, 250, 205)

    @classmethod
    def get_LightBlue(cls) -> 'Rgb':
        return cls(173, 216, 230)

    @classmethod
    def get_LightCoral(cls) -> 'Rgb':
        return cls(240, 128, 128)

    @classmethod
    def get_LightCyan(cls) -> 'Rgb':
        return cls(224, 255, 255)

    @classmethod
    def get_LightGoldenrodYellow(cls) -> 'Rgb':
        return cls(250, 250, 210)

    @classmethod
    def get_LightGray(cls) -> 'Rgb':
        return cls(211, 211, 211)

    @classmethod
    def get_LightGreen(cls) -> 'Rgb':
        return cls(144, 238, 144)

    @classmethod
    def get_LightPink(cls) -> 'Rgb':
        return cls(255, 182, 193)

    @classmethod
    def get_LightSalmon(cls) -> 'Rgb':
        return cls(255, 160, 122)

    @classmethod
    def get_LightSeaGreen(cls) -> 'Rgb':
        return cls(32, 178, 170)

    @classmethod
    def get_LightSkyBlue(cls) -> 'Rgb':
        return cls(135, 206, 250)

    @classmethod
    def get_LightSlateGray(cls) -> 'Rgb':
        return cls(119, 136, 153)

    @classmethod
    def get_LightSteelBlue(cls) -> 'Rgb':
        return cls(176, 196, 222)

    @classmethod
    def get_LightYellow(cls) -> 'Rgb':
        return cls(255, 255, 224)

    @classmethod
    def get_Lime(cls) -> 'Rgb':
        return cls(0, 255, 0)

    @classmethod
    def get_LimeGreen(cls) -> 'Rgb':
        return cls(50, 205, 50)

    @classmethod
    def get_Linen(cls) -> 'Rgb':
        return cls(250, 240, 230)

    @classmethod
    def get_Magenta(cls) -> 'Rgb':
        return cls(255, 0, 255)

    @classmethod
    def get_Maroon(cls) -> 'Rgb':
        return cls(128, 0, 0)

    @classmethod
    def get_MediumAquamarine(cls) -> 'Rgb':
        return cls(102, 205, 170)

    @classmethod
    def get_MediumBlue(cls) -> 'Rgb':
        return cls(0, 0, 205)

    @classmethod
    def get_MediumOrchid(cls) -> 'Rgb':
        return cls(186, 85, 211)

    @classmethod
    def get_MediumPurple(cls) -> 'Rgb':
        return cls(147, 112, 219)

    @classmethod
    def get_MediumSeaGreen(cls) -> 'Rgb':
        return cls(60, 179, 113)

    @classmethod
    def get_MediumSlateBlue(cls) -> 'Rgb':
        return cls(123, 104, 238)

    @classmethod
    def get_MediumSpringGreen(cls) -> 'Rgb':
        return cls(0, 250, 154)

    @classmethod
    def get_MediumTurquoise(cls) -> 'Rgb':
        return cls(72, 209, 204)

    @classmethod
    def get_MediumVioletRed(cls) -> 'Rgb':
        return cls(199, 21, 133)

    @classmethod
    def get_MidnightBlue(cls) -> 'Rgb':
        return cls(25, 25, 112)

    @classmethod
    def get_MintCream(cls) -> 'Rgb':
        return cls(245, 255, 250)

    @classmethod
    def get_MistyRose(cls) -> 'Rgb':
        return cls(255, 228, 225)

    @classmethod
    def get_Moccasin(cls) -> 'Rgb':
        return cls(255, 228, 181)

    @classmethod
    def get_NavajoWhite(cls) -> 'Rgb':
        return cls(255, 222, 173)

    @classmethod
    def get_Navy(cls) -> 'Rgb':
        return cls(0, 0, 128)

    @classmethod
    def get_OldLace(cls) -> 'Rgb':
        return cls(253, 245, 230)

    @classmethod
    def get_Olive(cls) -> 'Rgb':
        return cls(128, 128, 0)

    @classmethod
    def get_OliveDrab(cls) -> 'Rgb':
        return cls(107, 142, 35)

    @classmethod
    def get_Orange(cls) -> 'Rgb':
        return cls(255, 165, 0)

    @classmethod
    def get_OrangeRed(cls) -> 'Rgb':
        return cls(255, 69, 0)

    @classmethod
    def get_Orchid(cls) -> 'Rgb':
        return cls(218, 112, 214)

    @classmethod
    def get_PaleGoldenrod(cls) -> 'Rgb':
        return cls(238, 232, 170)

    @classmethod
    def get_PaleGreen(cls) -> 'Rgb':
        return cls(152, 251, 152)

    @classmethod
    def get_PaleTurquoise(cls) -> 'Rgb':
        return cls(175, 238, 238)

    @classmethod
    def get_PaleVioletRed(cls) -> 'Rgb':
        return cls(219, 112, 147)

    @classmethod
    def get_PapayaWhip(cls) -> 'Rgb':
        return cls(255, 239, 213)

    @classmethod
    def get_PeachPuff(cls) -> 'Rgb':
        return cls(255, 218, 185)

    @classmethod
    def get_Peru(cls) -> 'Rgb':
        return cls(205, 133, 63)

    @classmethod
    def get_Pink(cls) -> 'Rgb':
        return cls(255, 192, 203)

    @classmethod
    def get_Plum(cls) -> 'Rgb':
        return cls(221, 160, 221)

    @classmethod
    def get_PowderBlue(cls) -> 'Rgb':
        return cls(176, 224, 230)

    @classmethod
    def get_Purple(cls) -> 'Rgb':
        return cls(128, 0, 128)

    @classmethod
    def get_Red(cls) -> 'Rgb':
        return cls(255, 0, 0)

    @classmethod
    def get_RosyBrown(cls) -> 'Rgb':
        return cls(188, 143, 143)

    @classmethod
    def get_RoyalBlue(cls) -> 'Rgb':
        return cls(65, 105, 225)

    @classmethod
    def get_SaddleBrown(cls) -> 'Rgb':
        return cls(139, 69, 19)

    @classmethod
    def get_Salmon(cls) -> 'Rgb':
        return cls(250, 128, 114)

    @classmethod
    def get_SandyBrown(cls) -> 'Rgb':
        return cls(244, 164, 96)

    @classmethod
    def get_SeaGreen(cls) -> 'Rgb':
        return cls(46, 139, 87)

    @classmethod
    def get_SeaShell(cls) -> 'Rgb':
        return cls(255, 245, 238)

    @classmethod
    def get_Sienna(cls) -> 'Rgb':
        return cls(160, 82, 45)

    @classmethod
    def get_Silver(cls) -> 'Rgb':
        return cls(192, 192, 192)

    @classmethod
    def get_SkyBlue(cls) -> 'Rgb':
        return cls(135, 206, 235)

    @classmethod
    def get_SlateBlue(cls) -> 'Rgb':
        return cls(106, 90, 205)

    @classmethod
    def get_SlateGray(cls) -> 'Rgb':
        return cls(112, 128, 144)

    @classmethod
    def get_Snow(cls) -> 'Rgb':
        return cls(255, 250, 250)

    @classmethod
    def get_SpringGreen(cls) -> 'Rgb':
        return cls(0, 255, 127)

    @classmethod
    def get_SteelBlue(cls) -> 'Rgb':
        return cls(70, 130, 180)

    @classmethod
    def get_Tan(cls) -> 'Rgb':
        return cls(210, 180, 140)

    @classmethod
    def get_Teal(cls) -> 'Rgb':
        return cls(0, 128, 128)

    @classmethod
    def get_Thistle(cls) -> 'Rgb':
        return cls(216, 191, 216)

    @classmethod
    def get_Tomato(cls) -> 'Rgb':
        return cls(255, 99, 71)

    @classmethod
    def get_Turquoise(cls) -> 'Rgb':
        return cls(64, 224, 208)

    @classmethod
    def get_Violet(cls) -> 'Rgb':
        return cls(238, 130, 238)

    @classmethod
    def get_Wheat(cls) -> 'Rgb':
        return cls(245, 222, 179)

    @classmethod
    def get_White(cls) -> 'Rgb':
        return cls(255, 255, 255)

    @classmethod
    def get_WhiteSmoke(cls) -> 'Rgb':
        return cls(245, 245, 245)

    @classmethod
    def get_Yellow(cls) -> 'Rgb':
        return cls(255, 255, 0)

    @classmethod
    def get_YellowGreen(cls) -> 'Rgb':
        return cls(154, 205, 50)
