import math

from .sim_consts import *


def distance(this, that):
    a = this.position
    b = that.position
    return math.hypot(a.x - b.x, a.y - b.y)


def detect_colisions(plane, missiles):

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
            if distance(missile, other) < HIT_RADIUS:
                hit_list.append(missile.position)

                missile.hit()
                other.hit()
    return hit_list
