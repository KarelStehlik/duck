import numba
import pyglet
import time
import random
from pyglet.window import key
from pyglet import clock
import os
import math
from numba import njit, float64
import constants

def get_fitness(obj):
    return obj.fitness

groups = [pyglet.graphics.OrderedGroup(i) for i in range(20)]
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)

def is_empty_2d(l):
    for e in l:
        if e:
            return False
    return True


@njit
def average(*a):
    s = 0
    for e in a:
        s += e
    return s / len(a)


average(*[1.1, 1.1, 1.2])


@njit
def point_line_dist(x, y, normal_vector, c):
    # assumes vector is normalized
    return abs(x * normal_vector[0] + y * normal_vector[1] + c)


point_line_dist(1.1, 1.1, (1.1, 1.1), 1.1)

@njit
def get_rotation(x, y):
    if x==0 and y==0:
        return 0
    inv_hypot = (x ** 2 + y ** 2) ** -.5
    if x >= 0:
        return math.asin(max(min(y * inv_hypot, 1), -1))
    return math.pi - math.asin(max(min(y * inv_hypot, 1), -1))


get_rotation(1.1, 1.1)


@njit
def get_rotation_norm(x, y):
    if x >= 0:
        return math.asin(max(min(y, 1), -1))
    return math.pi - math.asin(max(min(y, 1), -1))


get_rotation_norm(.1, .1)


@njit
def inv_h(x, y):
    return (x ** 2 + y ** 2) ** -.5


inv_h(1.1, 1.1)


@njit
def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5


distance(1.1, 1.1, 1.1, 1.1)


@njit  # (List(float64))
def product(*a):
    if len(a) == 0:
        return 1.0
    p = 1.0
    for e in a:
        p *= e
    return p


product(1.2, 1.3, 1.2)
