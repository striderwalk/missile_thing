from plane_game import PlaneGame
import math


def distance(this, that):

    return math.hypot(this.x - that.x, this.y - that.y)


def control_plane(plane, missiles):

    if not missiles:
        return

    nearest = min(missiles, key=lambda x: distance(x.position, plane.position))

    if distance(nearest.position, plane.position) < 55:
        return plane.heading + math.pi / 16


from plane_game import PlaneGame

game = PlaneGame(control_plane)
score = game.run()
print(score)
