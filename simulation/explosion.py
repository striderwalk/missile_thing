import pygame


from ..colours import *


class Explosion:
    def __init__(self, position):

        self.position = position
        self.lifetime = 10
        self.active = True

    def get_image(self):
        surface = pygame.Surface((40, 40), pygame.SRCALPHA)

        surface.fill((0, 0, 0, 0))
        pygame.draw.circle(surface, RED, (20, 20), 15)
        return surface

    def update(self):
        self.lifetime -= 1
        if self.lifetime < 0:
            self.active = False


class Explosions:
    def __init__(self):

        self.explosions = []

    def add(self, position):
        self.explosions.append(Explosion(position))

    def remove(self, explosion):
        self.explosions.remove(explosion)

    def update(self):
        removals = []
        for explosion in self.explosions:
            if explosion.active:

                explosion.update()
            else:
                removals.append(explosion)

        for explosion in removals:
            self.remove(explosion)

    def draw(self, win, camera):
        for explosion in self.explosions:
            win.blit(explosion.get_image(), camera.apply(explosion.position))
