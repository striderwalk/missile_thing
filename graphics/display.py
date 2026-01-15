import pygame

from . import Camera, make_background
from .disp_consts import *


class Display:

    def __init__(self):
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.camera = Camera()

    def update(self, sim):

        pygame.display.flip()

        background = make_background(self.camera.position)
        self.win.blit(background, (0, 0))

        self.camera.update(sim.plane)

        sim.plane.draw(self.win, self.camera)
        sim.missiles.draw(self.win, self.camera)
        sim.explosions.draw(self.win, self.camera)

        # pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    return False

        return True
