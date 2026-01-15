import math
import random
import time

import pygame
from pygame.locals import *

from camera import Camera
from clouds import make_background
from collisions import detect_colisions
from consts import *
from explosion import Explosions
from missile import Missiles
from plane import Plane, control_plane

random.seed(1)


def main(display=True):

    pygame.init()
    clock = pygame.time.Clock()

    if display:
        myfont = pygame.font.SysFont("Arial", 32)
        win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        camera = Camera()

    plane = Plane(pygame.math.Vector2(0, 0))
    missiles = Missiles()
    missiles.spawn_missile(plane)
    explosions = Explosions()

    run = True
    start_time = pygame.time.get_ticks()
    while run:
        
        dt = clock.tick(FPS)

        if display:
            pygame.display.flip()

        control_plane(plane, missiles.get_visable(plane))

        # Updates
        alive = plane.update(dt)
        run = alive
        missiles.update(dt, plane)
        explosions.update()

        # Colisions
        colisions = detect_colisions(plane, missiles)
        for colision in colisions:
            explosions.add(colision)

        # Draw
        if not display:
            continue

        camera.update(plane)
        # Clouds ect.
        background = make_background(camera.position)
        win.blit(background, (0, 0))

        # others
        win.blit(plane.get_image(), camera.apply(plane.position))
        missiles.draw(win, camera)
        explosions.draw(win, camera)

        # debug
        label = myfont.render(
            f"HITS:{plane.hits:>3}, FPS:{clock.get_fps():.2f}",
            1,
            (128, 255, 128),
        )
        win.blit(label, (10, 10))

        # pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    run = False

    end_time = pygame.time.get_ticks()
    pygame.quit()

    return math.floor((end_time - start_time) / 1000)


if __name__ == "__main__":
<<<<<<< HEAD
    print(main())
=======
    main(False)
>>>>>>> 2ab6a07ba23aa5436473162c9e0447d0b8e2aaed
