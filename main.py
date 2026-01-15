from plane_game import PlaneGame
import math

"""
plane:
    position
    heading
    target_heading


missiles:
    position
    id
    

 """


def distance(this, that):
    print(f"{this=}, {that=}")
    return math.hypot(this.x - that.x, this.y - that.y)


def control_plane(plane, missiles):

    if not missiles:
        return

    nearest = min(missiles, key=lambda x: distance(x.position, plane.position))

    if distance(nearest.position, plane.position) < 55:
        return plane.heading + math.pi / 4


game = PlaneGame(control_plane)
print(game.run())
