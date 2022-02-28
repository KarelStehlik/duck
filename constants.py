import pyglet

display = pyglet.canvas.Display()
screen = display.get_default_screen()
SCREEN_WIDTH = screen.width
SCREEN_HEIGHT = screen.height
SPRITE_SIZE_MULT = SCREEN_WIDTH / 1920
POOL_X, POOL_Y = int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)
POOL_RADIUS = int(SCREEN_HEIGHT * .42)
FOX_SIZE = 50
NETWORK_PARAMS = [4, [6, 6], 1]
MAX_TIME = 15000
POPULATION_SIZE = 100
MUTATIONS = 5
SHOWN = 1
INFINITY = 10 ** 30
SHOWN_RATIO = POPULATION_SIZE / SHOWN
KEEP_DUCKS = 5
WINS_TO_PROGRESS = 0.7
