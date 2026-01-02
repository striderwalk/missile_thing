import hashlib
import random

import pygame
from noise import pnoise2

from consts import *

# seed = random.randint(1, 1000)
seed = 1


def rand01(x, y, seed=0):
    key = f"{x},{y},{seed}".encode()
    h = hashlib.sha256(key).digest()
    return int.from_bytes(h, "big") / 2**256


def local_density(x, y, base_density):
    n = (pnoise2(x * 0.01, y * 0.01, base=seed) + 1) / 2
    return base_density * n


def has_point(x, y, base_density):
    return rand01(x, y, 9999) < local_density(x, y, base_density)


def make_backgroud(world_position):
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface.fill(SKY_BLUE)

    for x in range(0, SCREEN_WIDTH, 10):
        for y in range(0, SCREEN_HEIGHT, 10):
            if has_point(world_position.x + x, world_position.y + y, CLOUD_DENSITY):
                pygame.draw.circle(surface, WHITE, (x, y), 10)

    return surface
