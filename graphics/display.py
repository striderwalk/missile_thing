import pygame

from . import Camera, Background
from .disp_consts import *


class Display:

    def __init__(self):
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.camera = Camera()
        self.debug_veiw = False
        self.background = Background()

    def update(self, sim) -> bool:

        pygame.display.flip()

        self.camera.update(sim.plane)

        self.background.update(self.camera.rect)

        self.background.draw(self.win, self.camera, self.debug_veiw)
        sim.plane.draw(self.win, self.camera, self.debug_veiw)
        sim.missiles.draw(self.win, self.camera, self.debug_veiw)

        sim.explosions.draw(self.win, self.camera)

        # pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    return False

                if event.key == pygame.K_d:

                    self.debug_veiw = not self.debug_veiw

        return True
