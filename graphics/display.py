import pygame

from . import Camera, make_background
from .disp_consts import *


class Display:

    def __init__(self):
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.camera = Camera()
        self.debug_veiw = False

    def update(self, sim) -> bool:

        pygame.display.flip()

        background = make_background(self.camera.position)
        self.win.blit(background, (0, 0))

        self.camera.update(sim.plane)

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
