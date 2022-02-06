from pyglet.gl import *

import groups
import images
from constants import *
from pyglet.window import key


def sprite_with_scale(img, scale, scale_x, scale_y, *args, **kwargs) -> pyglet.sprite.Sprite:
    a = pyglet.sprite.Sprite(img, *args, **kwargs)
    a.update(scale=scale, scale_x=scale_x, scale_y=scale_y)
    return a


class TextureEnableGroup(pyglet.graphics.OrderedGroup):
    def set_state(self):
        glEnable(GL_TEXTURE_2D)

    def unset_state(self):
        glDisable(GL_TEXTURE_2D)


texture_enable_groups = [TextureEnableGroup(i) for i in range(10)]


class TextureBindGroup(pyglet.graphics.Group):
    def __init__(self, texture, layer=0):
        super(TextureBindGroup, self).__init__(parent=texture_enable_groups[layer])
        self.texture = texture

    def set_state(self):
        glBindTexture(GL_TEXTURE_2D, self.texture.id)

    # No unset_state method required.
    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self.texture.id == other.texture.id and
                self.texture.target == other.texture.target and
                self.parent == other.parent)

    def __hash__(self):
        return hash((self.texture.id, self.texture.target))


def do_nothing(*args):
    pass


class text_box:
    def __init__(self, func, x, y, width, height, batch, image=images.Button, default=0, args=(), layer=5):
        self.sprite = pyglet.sprite.Sprite(image, x=x + width / 2, y=y + height / 2, batch=batch, group=groups.g[layer])
        self.layer = layer
        self.sprite.scale_x = width / self.sprite.width
        self.sprite.scale_y = height / self.sprite.height
        self.func = func
        self.fargs = args
        self.batch = batch
        self.x, self.y, self.width, self.height = x, y, width, height
        self.ogx, self.ogy = x, y
        self.text = pyglet.text.Label(str(default), x=self.x + self.width // 2,
                                      y=self.y + self.height * 4 / 7, color=(255, 255, 0, 255),
                                      batch=batch, group=groups.g[layer + 1], font_size=int(self.height / 2),
                                      anchor_x="center", align="center", anchor_y="center")
        self.down = False
        self.big = 0
        self.selected = False
        self.value = default
        self.in_decimals = 0

    def hide(self):
        self.text.batch = None
        self.sprite.batch = None

    def show(self):
        self.text.batch = self.batch
        self.sprite.batch = self.batch

    def set_image(self, img):
        self.sprite = pyglet.sprite.Sprite(img, x=self.x + self.width / 2, y=self.y + self.height / 2,
                                           batch=self.batch,
                                           group=groups.g[self.layer])
        self.sprite.scale_x = self.width / self.sprite.width
        self.sprite.scale_y = self.height / self.sprite.height

    def update(self, x, y):
        self.sprite.update(x=x + self.width / 2, y=y + self.height / 2)
        self.x, self.y = x, y
        self.text.x = x + self.width // 2
        self.text.y = y + self.height * 4 / 7

    def mouse_click(self, x, y):
        if self.x + self.width >= x >= self.x and self.y + self.height >= y >= self.y:
            self.selected = True
            self.value = 0
            self.in_decimals=0
            self.text.text=""
            return True
        if self.selected:
            if not self.value==0:
                self.func(self.value)
            self.selected = False
        return False

    def delete(self):
        self.sprite.delete()
        self.text.delete()

    def update_text(self):
        self.text.text = str(self.value)

    def key_press(self, symbol):
        if self.selected:
            if key.NUM_9 >= symbol >= key.NUM_0:
                if self.in_decimals == 0:
                    self.value *= 10
                    self.value += symbol - key.NUM_0
                else:
                    self.value += (symbol - key.NUM_0) * 10 ** -self.in_decimals
                    self.in_decimals += 1
                self.update_text()
            elif symbol==key.PERIOD:
                if self.in_decimals==0:
                    self.in_decimals=1
            elif symbol==key.ENTER:
                self.func(self.value)
                self.selected=False


class button:
    def __init__(self, func, x, y, width, height, batch, image=images.Button, text="", args=(), layer=5,
                 mouseover=do_nothing, mouseoff=do_nothing, mover_args=(), moff_args=()):
        self.sprite = pyglet.sprite.Sprite(image, x=x + width / 2, y=y + height / 2, batch=batch, group=groups.g[layer])
        self.layer = layer
        self.sprite.scale_x = width / self.sprite.width
        self.sprite.scale_y = height / self.sprite.height
        self.func = func
        self.fargs = args
        self.batch = batch
        self.x, self.y, self.width, self.height = x, y, width, height
        self.ogx, self.ogy = x, y
        self.text = pyglet.text.Label(text, x=self.x + self.width // 2,
                                      y=self.y + self.height * 4 / 7, color=(255, 255, 0, 255),
                                      batch=batch, group=groups.g[layer + 1], font_size=int(self.height / 2),
                                      anchor_x="center", align="center", anchor_y="center")
        self.down = False
        self.big = 0
        self.on_mouse_over = mouseover
        self.on_mouse_off = mouseoff
        self.mover_args = mover_args
        self.moff_args = moff_args

    def hide(self):
        self.text.batch = None
        self.sprite.batch = None

    def show(self):
        self.text.batch = self.batch
        self.sprite.batch = self.batch

    def set_image(self, img):
        self.sprite = pyglet.sprite.Sprite(img, x=self.x + self.width / 2, y=self.y + self.height / 2, batch=self.batch,
                                           group=groups.g[self.layer])
        self.sprite.scale_x = self.width / self.sprite.width
        self.sprite.scale_y = self.height / self.sprite.height

    def embiggen(self):
        self.big = 1
        self.sprite.scale = 1.1

    def unbiggen(self):
        self.big = 0
        self.sprite.scale = 1

    def smallen(self):
        self.big = -1
        self.sprite.scale = 0.9

    def update(self, x, y):
        self.sprite.update(x=x + self.width / 2, y=y + self.height / 2)
        self.x, self.y = x, y
        self.text.x = x + self.width // 2
        self.text.y = y + self.height * 4 / 7

    def mouse_move(self, x, y):
        if not self.down:
            if (self.big == 1) == (self.x + self.width >= x >= self.x and self.y + self.height >= y >= self.y):
                return
            if self.big != 1:
                self.mouse_over()
                return
            self.mouse_off()

    def mouse_over(self):
        self.embiggen()
        self.on_mouse_over(*self.mover_args)

    def mouse_off(self):
        self.unbiggen()
        self.on_mouse_off(*self.moff_args)

    def mouse_click(self, x, y):
        if self.x + self.width >= x >= self.x and self.y + self.height >= y >= self.y:
            self.smallen()
            self.down = True
            return True
        return False

    def mouse_release(self, x, y):
        if self.down:
            self.down = False
            self.unbiggen()
            if self.x + self.width >= x >= self.x and self.y + self.height >= y >= self.y:
                self.func(*self.fargs)

    def delete(self):
        self.sprite.delete()
        self.text.delete()
