from terrex.net.rgb import Rgb as Color

def paint_color(color: int) -> Color:
    white = Color(255, 255, 255)
    num = color
    if num == 1 or num == 13:
        return Color(255, 0, 0)
    if num == 2 or num == 14:
        return Color(255, 127, 0)
    if num == 3 or num == 15:
        return Color(255, 255, 0)
    if num == 4 or num == 16:
        return Color(127, 255, 0)
    if num == 5 or num == 17:
        return Color(0, 255, 0)
    if num == 6 or num == 18:
        return Color(0, 255, 127)
    if num == 7 or num == 19:
        return Color(0, 255, 255)
    if num == 8 or num == 20:
        return Color(0, 127, 255)
    if num == 9 or num == 21:
        return Color(0, 0, 255)
    if num == 10 or num == 22:
        return Color(127, 0, 255)
    if num == 11 or num == 23:
        return Color(255, 0, 255)
    if num == 12 or num == 24:
        return Color(255, 0, 127)
    if num == 25:
        return Color(75, 75, 75)
    if num == 26:
        return Color(255, 255, 255)
    if num == 27:
        return Color(175, 175, 175)
    if num == 28:
        return Color(255, 178, 125)
    if num == 29:
        return Color(25, 25, 25)
    if num == 30:
        return Color(200, 200, 200, 150)
    return white
