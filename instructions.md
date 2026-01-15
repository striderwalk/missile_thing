Write a function that takes two arguments plane and missiles and returns a new target heading for the plane based on the positions of the missiles. If `None` is returned the plane will keep its current target heading.

The plane travels at a constant speed of (100 m/s) and can turn at $\pi$ radians per second. Missiles can travel at 150 m/s but can only turn at $\frac{1}{2}\pi$ radians per second.
The planes visible range is 150m in every direction, but between $\frac{1}{6}\pi$ radians either side of its current heading it can see up to 300m.

```python
from plane_game import PlaneGame


def control(plane, missiles):
    # usage example:
    plane.position # vector2 from pygame-ce
    plane.heading  # in radians
    plane.target_heading  # in radians

    missiles #  list of missile objects
    for missile in missiles:
        missile.position  # vector2
        missile.id   # a unique identifier


```

This is the code needed to run the game with your control function. By default this will launch a window to see the game, to disable the window pass `render=False` to `PlaneGame`.

```python
game = PlaneGame(control)
score = game.run()

```

The heading is in radians, 0 represents moving in the positive y direction (up on the screen), increasing the angle will rotate clockwise.

Your score is the number of seconsds you survive before you lose all your health. You will die after being hit 3 times.
