from constants import *


def RI(name, centre=True):
    a = pyglet.resource.image(f"imagefolder/{name}.png")
    if centre:
        centre_anchor(a)
    return a


def IL(name, centre=True):
    a = pyglet.image.load(f"imagefolder/{name}.png")
    if centre:
        centre_anchor(a)
    return a


def centre_anchor(e):
    e.anchor_x = e.width // 2
    e.anchor_y = e.height // 2


Background = IL("Background").get_texture()
Fox = RI("Fox")
Duck = RI("Duck")
Pool = RI("Pool")
Button = RI("Button")
Ring=RI("Ring")
