from PIL import Image, ImageDraw
from progressbar import ETA, Bar, FileTransferSpeed, Percentage, ProgressBar, RotatingMarker

from terrex.world.world import World


def draw_world(world: World):
    height = len(world.tiles)
    width = len(world.tiles[0]) if height > 0 else 0
    image = Image.new("RGB", (width, height), "white")
    imgdraw = ImageDraw.Draw(image)
    widgets = ['Percentage: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' Speed: ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=height).start()

    if height == 0:
        pbar.finish()
        return

    x = 0
    y = 0
    for j in world.tiles:
        for i in j:
            if i is None:
                continue
            color = (int(i.type), int(i.type), int(i.type))
            imgdraw.point((x, y), fill=color)
            x += 1
        x = 0
        y += 1
        pbar.update(y)
    pbar.finish()
    image.show()
