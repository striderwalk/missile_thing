import math


def distance(this, that):
    a = this.position
    b = that.position
    return math.hypot(a.x - b.x, a.y - b.y)


def control_plane(plane, missiles):

    if not missiles:
        return
    nearest = min(missiles, key=lambda x: distance(x, plane))

    if distance(nearest, plane) < 55:
        plane.set_target_heading(plane.heading + math.pi / 4)
