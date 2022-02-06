import client_utility
import constants
from constants import *
from imports import *
import images
import groups
import neurons


class Game:
    def __init__(self, window):
        self.boost = False
        self.starttime = time.perf_counter()
        self.ticks = 0
        self.fps = 144
        self.generations = 0
        self.batch = window.batch
        self.mouseheld = False
        self.window = window
        self.keys = window.keys
        self.mouse_x, self.mouse_y = 0, 0
        self.speed = 30
        self.speed_ratio = 0.5
        self.ducks = [Duck(self, neurons.Network(*constants.NETWORK_PARAMS), e % constants.SHOWN_RATIO == 0)
                      for e in range(constants.POPULATION_SIZE)]
        self.foxes = [Fox(self, e, e.visible) for e in self.ducks]
        self.ongoing = True
        self.background_texgroup = client_utility.TextureBindGroup(images.Background, layer=0)
        self.background = self.batch.add(
            4, pyglet.gl.GL_QUADS, self.background_texgroup,
            ("v2i", (0, 0, SCREEN_WIDTH, 0,
                     SCREEN_WIDTH, SCREEN_HEIGHT, 0, SCREEN_HEIGHT)),
            ("t2f", (0, 0, SCREEN_WIDTH / 512, 0, SCREEN_WIDTH / 512, SCREEN_HEIGHT / 512,
                     0, SCREEN_HEIGHT / 512))
        )
        self.pool = pyglet.sprite.Sprite(images.Pool, x=POOL_X, y=POOL_Y, batch=self.batch, group=groups.g[1])
        self.pool.scale = POOL_RADIUS * 2 / self.pool.width
        self.ring = pyglet.sprite.Sprite(images.Ring, x=POOL_X, y=POOL_Y, batch=self.batch, group=groups.g[2])
        self.ring.scale = POOL_RADIUS * 2 / self.ring.width / self.speed_ratio
        self.result_text = None
        self.duration = 0
        self.textboxes = [(client_utility.text_box(self.set_speed, SCREEN_WIDTH * .8, SCREEN_HEIGHT * .9,
                                                   SCREEN_WIDTH * .2, SCREEN_HEIGHT * .1,
                                                   self.batch, default=self.speed)),
                          ]
        self.labels = [pyglet.text.Label(
            "overall speed",
            x=SCREEN_WIDTH * .79,
            y=SCREEN_HEIGHT * .95, color=(255, 255, 255, 255),
            batch=self.batch, group=groups.g[3], font_size=int(SCREEN_HEIGHT * .03),
            anchor_x="right", align="center", anchor_y="center"),
            pyglet.text.Label(
                f"fox / duck speed: {self.speed_ratio}",
                x=SCREEN_WIDTH * .98,
                y=SCREEN_HEIGHT * .85, color=(255, 255, 255, 255),
                batch=self.batch, group=groups.g[3], font_size=int(SCREEN_HEIGHT * .03),
                anchor_x="right", align="center", anchor_y="center"),
            pyglet.text.Label(
                "generation 0",
                x=SCREEN_WIDTH * .02,
                y=SCREEN_HEIGHT * .95, color=(255, 255, 255, 255),
                batch=self.batch, group=groups.g[3], font_size=int(SCREEN_HEIGHT * .03),
                anchor_x="left", align="center", anchor_y="center")
        ]

    def set_speed(self, speed):
        self.speed = speed
        for e in self.ducks:
            e.speed = speed
        for e in self.foxes:
            e.angular_speed = speed * self.speed_ratio / POOL_RADIUS

    def set_speed_ratio(self, ratio):
        self.ring.scale = POOL_RADIUS * 2 / images.Ring.width / ratio
        self.speed_ratio = ratio
        for e in self.foxes:
            e.angular_speed = self.speed * ratio / POOL_RADIUS
        self.labels[1].text = f"fox / duck speed: {round(self.speed_ratio, 2)}"

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x, self.mouse_y = x + dx, y + dy

    def on_mouse_drag(self, x, y, dx, dy):
        self.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        [e.key_press(symbol) for e in self.textboxes]
        if symbol == key.B:
            self.boost = not self.boost

    def on_key_release(self, s, m):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        self.mouseheld = False

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouseheld = True
        [e.mouse_click(x, y) for e in self.textboxes]

    def tick(self):
        t0 = time.perf_counter()
        if self.ongoing and time.perf_counter() - self.starttime > self.ticks / self.fps:
            self.tick2()
            self.ticks += 1
            while self.boost and (time.perf_counter() - t0 < 0.5):
                self.tick2()
        [e.graphics_update() for e in self.ducks]
        [e.graphics_update() for e in self.foxes]

    def tick2(self):
        self.duration += self.speed
        [e.tick() for e in self.ducks]
        [e.tick() for e in self.foxes]
        if self.duration > constants.MAX_TIME or True not in [e.active for e in self.ducks]:
            self.new_round()

    def new_round(self):
        self.generations += 1
        [e.deactivate() for e in self.ducks]
        wins = 0
        for e in self.ducks:
            if e.fitness > constants.INFINITY:
                wins += 1
        if wins > 0.7 * constants.POPULATION_SIZE:
            self.set_speed_ratio(self.speed_ratio + 0.05)
        self.ducks.sort(key=get_fitness, reverse=True)
        d = []
        i = 0
        self.duration = 0
        for e in range(constants.KEEP_DUCKS):
            d.append(Duck(self,self.ducks[e].ai.clone(),False))
        while len(d) < constants.POPULATION_SIZE:
            child1 = self.ducks[i].ai
            child2 = self.ducks[i].ai.clone()
            child1.mutate(constants.MUTATIONS)
            child2.mutate(constants.MUTATIONS)
            d.append(Duck(self, child1, i % (constants.SHOWN_RATIO // 2) == 0))
            d.append(Duck(self, child2, False))
            i += 1
        [e.delete() for e in self.foxes]
        self.foxes = [Fox(self, e, e.visible) for e in d]
        self.ducks = d
        self.labels[2].text = f"generation {self.generations}"


def get_fitness(obj):
    return obj.fitness


class Duck:
    def __init__(self, game, ai, visible=True):
        self.game = game
        self.x = POOL_X
        self.y = POOL_Y
        self.speed = game.speed
        self.visible = visible
        if visible:
            self.sprite = pyglet.sprite.Sprite(images.Duck, x=self.x, y=self.y, batch=game.batch, group=groups.g[3])
            self.sprite.scale = SCREEN_WIDTH * .05 / self.sprite.width
            self.sprite.opacity = 100
        self.ai = ai
        self.fox = None
        self.fitness = 0
        self.active = True
        self.direction = 0
        self.rush = False

    def tick(self):
        if not self.active:
            return
        fox_angle = self.fox.angle
        centre_distance = distance(self.x, self.y, POOL_X, POOL_Y)
        angle_to_fox = get_rotation(self.x - POOL_X, self.y - POOL_Y) - fox_angle

        self.fitness += abs(angle_to_fox + 2 * math.pi) % math.pi * 1000 - 5000
        if not self.rush:
            ai_output = self.ai.run([math.sin(angle_to_fox),
                                     math.cos(angle_to_fox),
                                     (POOL_RADIUS / self.game.speed_ratio - centre_distance) / 1000,
                                     (constants.MAX_TIME - self.game.duration) / 1000],
                                    )
            ai_angle = ai_output[0]
           # self.rush = ai_output[1]
            self.direction = get_rotation(self.x - POOL_X, self.y - POOL_Y) + ai_angle / 100
        self.x += self.speed * math.cos(self.direction)
        self.y += self.speed * math.sin(self.direction)
        if centre_distance > POOL_RADIUS:
            self.deactivate()
            self.fitness += distance(self.x, self.y, self.fox.x, self.fox.y) * constants.INFINITY

    def graphics_update(self):
        if self.visible and self.active:
            self.sprite.update(rotation=90 - self.direction * 180 / math.pi, x=self.x, y=self.y)

    def die(self):
        self.deactivate()

    def deactivate(self):
        if self.active and self.visible:
            self.sprite.delete()
        self.active = False


class Fox:
    def __init__(self, game, target, visible=True):
        self.game = game
        self.x = POOL_X
        self.y = POOL_Y - POOL_RADIUS
        speed = game.speed * game.speed_ratio
        self.visible = visible
        if visible:
            self.sprite = pyglet.sprite.Sprite(images.Fox, x=self.x, y=self.y, batch=game.batch, group=groups.g[3])
            self.sprite.scale = SCREEN_WIDTH * .05 / self.sprite.width
            self.sprite.opacity = 100
        self.direction = 0
        self.angular_speed = speed / POOL_RADIUS
        self.angle = -math.pi / 2
        self.target = target
        self.target.fox = self

    def tick(self):
        if not self.target.active:
            return
        duck_angle = get_rotation(self.target.x - POOL_X, self.target.y - POOL_Y) % (2 * math.pi)
        if self.angle > duck_angle:
            direction = -1 if math.pi - self.angle + duck_angle > 0 else 1
        else:
            direction = -1 if duck_angle - self.angle > math.pi else 1
        self.angle += self.angular_speed * direction
        self.angle %= 2 * math.pi
        self.x, self.y = POOL_X + math.cos(self.angle) * POOL_RADIUS, POOL_Y + math.sin(self.angle) * POOL_RADIUS
        if distance(self.x, self.y, self.target.x, self.target.y) < FOX_SIZE:
            self.target.die()
            if self.visible:
                self.sprite.delete()
                self.visible = False

    def graphics_update(self):
        if self.visible and self.target.active:
            self.sprite.update(rotation=90 - self.angle * 180 / math.pi, x=self.x, y=self.y)

    def delete(self):
        try:
            self.sprite.delete()
        except AttributeError:
            pass