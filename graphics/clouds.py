from dataclasses import dataclass
import math

import pygame
from pygame.math import Vector2

from .disp_consts import *


from ..colours import *


def hash2d(x: int, y: int, seed: int = 0) -> float:
    cache: dict[tuple[int, int, int], float] = {}

    if (x, y, seed) in cache:
        return cache[(x, y, seed)]

    n = int(x * 374761393 + y * 668265263 + seed * 1442695040888963407)
    n = (n ^ (n >> 13)) * 1274126177
    n = n ^ (n >> 16)

    cache[(x, y, seed)] = (n & 0xFFFFFFFF) / 0x100000000

    return cache[(x, y, seed)]


def rect_difference(current: pygame.Rect, last: pygame.Rect) -> list[pygame.Rect]:
    # print(current, last)
    if not current.colliderect(last):
        return []

    overlapping_rect = current.clip(last)
    rect_diffences = []

    if overlapping_rect.top > current.top:
        rect_diffences.append(
            pygame.Rect(
                current.left,
                current.top,
                current.width,
                overlapping_rect.top - current.top,
            )
        )

    if overlapping_rect.bottom < current.bottom:
        rect_diffences.append(
            pygame.Rect(
                current.left,
                overlapping_rect.bottom,
                current.width,
                current.bottom - overlapping_rect.bottom,
            )
        )

    if overlapping_rect.left > current.left:
        rect_diffences.append(
            pygame.Rect(
                current.left,
                overlapping_rect.top,
                overlapping_rect.left - current.left,
                overlapping_rect.height,
            )
        )

    if overlapping_rect.right < current.right:
        rect_diffences.append(
            pygame.Rect(
                overlapping_rect.right,
                overlapping_rect.top,
                current.right - overlapping_rect.right,
                overlapping_rect.height,
            )
        )

    return rect_diffences


class Cloud:

    @classmethod
    def make(cls, grid_x: int, grid_y: int, cx: float, cy: float, seed: int) -> tuple:

        size = 0.6 + 0.8 * hash2d(grid_x, grid_y, seed + int(cx))
        shade = int(25 * hash2d(int(cx), grid_x & grid_y, seed - 3))

        return Cloud(Vector2(cx, cy), size, shade)

    def __init__(self, offset: Vector2, size: float, shade: int):
        self.offset = offset
        self.size = size
        self.shade = shade

    def __repr__(self):
        return f"Cloud offset by {self.offset}"


class CloudCluster:

    @classmethod
    def make(cls, grid_x, grid_y, seed=0):
        clouds = []
        offset_x = hash2d(grid_x, grid_y, seed + 1)
        offset_y = hash2d(grid_x, grid_y, seed + 2)

        root_x = (grid_x + offset_x) * CELL_SIZE
        root_y = (grid_y + offset_y) * CELL_SIZE
        position = Vector2(root_x, root_y)

        cluster_size = int(CLUSTER_SIZE * hash2d(grid_x, grid_y, seed + 1))

        for i in range(cluster_size):
            other_x = CLUSTER_SPREAD * (2 * hash2d(grid_x, grid_y, seed + i) - 0.5)
            other_y = CLUSTER_SPREAD * (2 * hash2d(grid_x, grid_y, seed - i) - 0.5)

            clouds.append(Cloud.make(grid_x, grid_y, other_x, other_y, seed))

        return CloudCluster(position, clouds)

    def __init__(self, position: Vector2, clouds: list[Cloud]):
        self.position = position
        self.clouds = clouds
        self.rect = pygame.Rect(
            position,
            4 * Vector2((CLOUD_SIZE + CLUSTER_SPREAD), (CLOUD_SIZE + CLUSTER_SPREAD)),
        )
        self.make_image()

    def draw_cloud(self, surface: pygame.Surface, cloud: Cloud):

        colour = tuple(i - cloud.shade for i in WHITE)

        pygame.draw.circle(
            surface,
            colour,
            Vector2(self.rect.width / 2, self.rect.height / 2) + cloud.offset,
            CLOUD_SIZE * cloud.size,
        )

    def make_image(self):
        surface = pygame.Surface(
            4 * Vector2((CLOUD_SIZE + CLUSTER_SPREAD), (CLOUD_SIZE + CLUSTER_SPREAD)),
            pygame.SRCALPHA,
        )
        for cloud in self.clouds:

            self.draw_cloud(
                surface,
                cloud,
            )

        self.image = surface

    def draw(self, surface: pygame.Surface, camera):
        surface.blit(self.image, camera.apply(self.rect.topleft))


class Background:
    def __init__(self):
        self.last_rect = pygame.Rect(
            -Vector2(SCREEN_WIDTH, SCREEN_HEIGHT) / 2, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.clusters = {}

    def draw(self, win: pygame.Surface, camera, debug_veiw=False):
        surface = pygame.Surface(
            (SCREEN_WIDTH + 400, SCREEN_HEIGHT + 400), pygame.SRCALPHA
        )

        surface.fill(SKY_BLUE)

        for cluster in self.clusters.values():

            cluster.draw(surface, camera)

        for diff in self.diffs:
            diff.center = camera.apply(diff.center)
            pygame.draw.rect(win, DEBUG_GREEN, diff, width=3)

        win.blit(surface, (0, 0))

    def add(self, cluster):
        self.clusters[tuple(cluster.position)] = cluster

    def add_clusters(self, clusters):
        for cluster in clusters:
            self.add(cluster)

    def remove(self, cluster):

        self.clusters.pop(tuple(cluster.position))

    def update(self, rect: pygame.Rect):

        rect = rect.scale_by(2.5)

        removals = []
        for cluster in self.clusters.values():

            if not rect.collidepoint(cluster.position):

                removals.append(cluster)

        for cluster in removals:
            self.remove(cluster)

        new_clusters = []
        diffs = rect_difference(rect, self.last_rect)
        self.diffs = diffs
        for diff in diffs:

            new_clusters.extend(find_clusters(diff))
        self.add_clusters(new_clusters)

        self.last_rect = rect.copy()


def find_clusters(rect: pygame.Rect, seed=0) -> list[CloudCluster]:

    clusters = []

    # Determine grid bounds
    x0 = math.floor((rect.left) / CELL_SIZE)
    x1 = math.ceil((rect.right) / CELL_SIZE)

    y0 = math.floor((rect.top) / CELL_SIZE)
    y1 = math.ceil((rect.bottom) / CELL_SIZE)

    for grid_x in range(x0, x1 + 1):
        for grid_y in range(y0, y1 + 1):

            h = hash2d(grid_x, grid_y, seed)
            if h > CLOUD_DENSITY:
                continue
            clusters.append(CloudCluster.make(grid_x, grid_y, seed))

    return clusters
