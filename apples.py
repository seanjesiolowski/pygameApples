import math
import random
from surface import SURFACE_WIDTH, SURFACE_HEIGHT

APPLE_RADIUS = 10


def make_apples(number):
    apples_array = []
    # make and keep making apples until number runs out
    while number > 0:
        rand_coor = (math.floor(random.random() * (SURFACE_WIDTH - APPLE_RADIUS) + APPLE_RADIUS),
                     math.floor(random.random() * (SURFACE_HEIGHT - APPLE_RADIUS) + APPLE_RADIUS))
        apple = [rand_coor, True]
        apples_array.append(apple)
        number -= 1
    return apples_array
