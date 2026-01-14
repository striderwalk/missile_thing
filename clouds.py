import math

import pygame
from pygame.math import Vector2 as Vector

from consts import *


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

    for gx in range(x0, x1 + 1):
        for gy in range(y0, y1 + 1):

            # Decide if this cell has a cloud
            h = hash2d(gx, gy, seed)
            if h < CLOUD_DENSITY:
                continue

            # Jitter inside the cell
            jx = hash2d(gx, gy, seed + 1)
            jy = hash2d(gx, gy, seed + 2)

            cx = (gx + jx) * CELL_SIZE
            cy = (gy + jy) * CELL_SIZE

            # Optional size variation
            size = 0.6 + 0.8 * hash2d(gx, gy, seed + 3)

            # Cull precisely to camera bounds
            if cam_x <= cx <= cam_x + cam_w and cam_y <= cy <= cam_y + cam_h:
                clouds.append((Vector(cx, cy), size))

    return clouds


def make_background(world_position, margin=1000):

    padded_surface = pygame.Surface(
        (SCREEN_WIDTH + margin * 2, SCREEN_HEIGHT + margin * 2), pygame.SRCALPHA
    )
    padded_surface.fill(SKY_BLUE)

    for cloud_position, cloud_size in get_clouds(
        world_position.x - margin,
        world_position.y - margin,
        SCREEN_WIDTH + margin * 2,
        SCREEN_HEIGHT + margin * 2,
        margin,
    ):

        pygame.draw.circle(
            padded_surface,
            WHITE,
            cloud_position - world_position + Vector(margin, margin),
            50 * cloud_size,
        )
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    surface.blit(padded_surface, (0, 0), (margin, margin, SCREEN_WIDTH, SCREEN_HEIGHT))

    return surface
