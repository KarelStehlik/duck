import pyglet

display = pyglet.canvas.Display()
screen = display.get_default_screen()
SCREEN_WIDTH = screen.width
SCREEN_HEIGHT = screen.height
SPRITE_SIZE_MULT = SCREEN_WIDTH / 1920
POOL_X, POOL_Y = int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)
POOL_RADIUS = int(SCREEN_HEIGHT * .42)
FOX_SIZE = SCREEN_WIDTH * .05
NETWORK_PARAMS = [4, [10, 10], 1]
MAX_TIME = 15000
POPULATION_SIZE = 150
MUTATIONS = 10
SHOWN = 5
INFINITY = 10 ** 30
SHOWN_RATIO = POPULATION_SIZE / SHOWN
KEEP_DUCKS = 5
