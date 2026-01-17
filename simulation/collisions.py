import math
from typing import List

from pygame import Vector2

from .sim_consts import *


def distance(this: Vector2, that: Vector2) -> float:

    return math.hypot(this.x - that.x, this.y - that.y)


def detect_colisions(plane, missiles) -> List[Vector2]:

    hit_list = []
    for missile in missiles:

        if missile.been_hit:
            continue
        if distance(missile, plane) < HIT_RADIUS:
            missile.hit()
            plane.hit()
            hit_list.append(missile.position)

        for other in missiles:
            if other.been_hit:
                continue
            if missile is other:
                continue
            if distance(missile.position, other.position) < HIT_RADIUS:
                hit_list.append(missile.position)

                missile.hit()
                other.hit()
    return hit_list
