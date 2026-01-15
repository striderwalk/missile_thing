import math

import pygame
from pygame.math import Vector2 as Vector

from .consts import *


def hash2d(x: int, y: int, seed: int = 0) -> float:
    """
    Deterministic hash from 2 ints → float in [0, 1)
    """
    n = int(x * 374761393 + y * 668265263 + seed * 1442695040888963407)
    n = (n ^ (n >> 13)) * 1274126177
    n = n ^ (n >> 16)
    return (n & 0xFFFFFFFF) / 0x100000000


def get_clouds(cam_x, cam_y, cam_w, cam_h, seed=1):

    clouds = []

    # Determine grid bounds
    x0 = math.floor((cam_x) / CELL_SIZE)
    y0 = math.floor((cam_y) / CELL_SIZE)

    x1 = math.floor((cam_x + cam_w) / CELL_SIZE)
    y1 = math.floor((cam_y + cam_h) / CELL_SIZE)

    for grid_x in range(x0, x1 + 1):
        for grid_y in range(y0, y1 + 1):

            # Decide if this cell has a cloud
            h = hash2d(grid_x, grid_y, seed)
            if h > CLOUD_DENSITY:
                continue

            # Jitter inside the cell
            jx = hash2d(grid_x, grid_y, seed + 1)
            jy = hash2d(grid_x, grid_y, seed + 2)

            cx = (grid_x + jx) * CELL_SIZE
            cy = (grid_y + jy) * CELL_SIZE

            clouds.append(make_cloud(grid_x, grid_y, cx, cy, seed))

            for i in range(int(CLUSTER_SIZE * hash2d(grid_x, grid_y, seed + 1))):
                other_x = CLUSTER_SPREAD * (2 * hash2d(grid_x, grid_y, seed + i) - 0.5)
                other_y = CLUSTER_SPREAD * (2 * hash2d(grid_x, grid_y, seed - i) - 0.5)
                clouds.append(
                    make_cloud(grid_x, grid_y, cx + other_x, cy + other_y, seed)
                )

    return clouds


def make_cloud(grid_x, grid_y, cx, cy, seed):

    size = 0.6 + 0.8 * hash2d(grid_x, grid_y, seed + int(cx))
    shade = int(50 * hash2d(int(cx), grid_x & grid_y, seed - 3))

    return (Vector(cx, cy), size, shade)


def make_background(world_position, margin=1000):

    padded_surface = pygame.Surface(
        (SCREEN_WIDTH + margin * 2, SCREEN_HEIGHT + margin * 2), pygame.SRCALPHA
    )
    padded_surface.fill(SKY_BLUE)

    for position, size, shade in get_clouds(
        world_position.x - margin,
        world_position.y - margin,
        SCREEN_WIDTH + margin * 2,
        SCREEN_HEIGHT + margin * 2,
        margin,
    ):
        colour = tuple(i - shade for i in WHITE)
        pygame.draw.circle(
            padded_surface,
            colour,
            position - world_position + Vector(margin, margin),
            CLOUD_SIZE * size,
        )
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    surface.blit(padded_surface, (0, 0), (margin, margin, SCREEN_WIDTH, SCREEN_HEIGHT))

    return surface
