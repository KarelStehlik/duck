import groups
import pyglet
import time
import os
import constants
import game
from pyglet.window import key

pyglet.options['debug_gl'] = False
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)


class windoo(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.sec = time.time()
        self.frames = 0
        self.fpscount = pyglet.text.Label(x=5, y=5, text="0", color=(255, 255, 255, 255),
                                          group=groups.g[9], batch=self.batch)
        self.mouseheld = False
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.last_tick = time.time()
        self.game = game.Game(self)

    def on_mouse_motion(self, x, y, dx, dy):
        self.game.on_mouse_motion(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.game.on_mouse_drag(x, y, dx, dy)

    def on_close(self):
        self.close()
        os._exit(0)

    def tick(self):
        self.dispatch_events()
        self.check()
        self.switch_to()
        self.clear()
        self.game.tick()
        self.batch.draw()
        self.flip()
        self.last_tick = time.time()

    def on_key_press(self, symbol, modifiers):
        self.game.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.game.on_key_release(symbol, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.mouseheld = False
        self.game.on_mouse_release(x, y, button, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouseheld = True
        self.game.on_mouse_press(x, y, button, modifiers)

    # def on_deactivate(self):
    #    self.minimize()

    def check(self):
        self.frames += 1
        if time.time() - self.sec >= 1:
            self.sec += 1
            self.fpscount.text = "fps: " + str(self.frames)
            self.frames = 0


place = windoo(caption='test', style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS, width=constants.SCREEN_WIDTH,
               height=constants.SCREEN_HEIGHT)
place.set_location(0, 0)

while True:
    place.tick()
    pyglet.clock.tick()
