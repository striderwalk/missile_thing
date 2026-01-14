import random
import math
import pygame
from pygame.math import Vector2 as Vector
from consts import *


def random_vector():
    t = random.uniform(0, 2 * math.pi)
    return Vector(math.cos(t), math.sin(t))


def distance(this, that):
    a = this.position
    b = that.position
    return math.hypot(a.x - b.x, a.y - b.y)


class Missile:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.acceleration = Vector(0, 0)
        self.has_seen_plane = False
        self.active = True
        self.been_hit = False
        self.lifetime = random.randint(25, 50)

        self.heading = 0
        self.target_heading = 0

        self.rect = pygame.Rect(self.x, self.y, 20, 20)

        self.los_angle = 0

    def get_image(self):
        surface = pygame.Surface((40, 40), pygame.SRCALPHA)

        surface.fill((255, 0, 0, 0))
        vel = self.velocity * 15 / FPS / 10

        pygame.draw.line(
            surface,
            (111, 111, 111),
            (20 - vel.x / 2, 20 - vel.y / 2),
            (20 + vel.x / 2, vel.y / 2 + 20),
            5,
        )
        if self.active:
            pygame.draw.circle(surface, (255, 128, 255), (20 + vel.x, 20 + vel.y), 2)

        return surface

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    def update_heading(self):
        dheading = self.heading - self.target_heading

        if abs(dheading) < MISSILE_TURNING_RADIUS:
            self.heading += dheading
        else:
            self.heading += MISSILE_TURNING_RADIUS * dheading / abs(dheading)

        new_x = math.sin(self.heading)
        new_y = math.cos(self.heading)
        self.velocity = Vector(new_x, new_y)

    def hit(self):
        self.been_hit = True
        self.active = False

    def limit_speed(self):
        self.velocity = self.velocity.normalize() * MISSILE_SPEED

    def set_target_heading(self, target):
        self.target_heading = target % (math.pi * 2)

    def update(self, dt, plane):

        self.lifetime -= dt
        if self.lifetime < 0:
            self.active = False
            return

        if distance(self, plane) > SPAWN_RADIUS * 1.5:
            self.active = False
            return

        if not self.active:
            return

        # upate movemnt
        self.update_heading()
        self.limit_speed()
        self.position += self.velocity * dt

        if distance(self, plane) < 35:
            self.has_seen_plane = True


class Missiles:

    def __init__(self):
        self.missiles = []

    def add(self, missile):
        self.missiles.append(missile)

    def remove(self, missile):
        self.missiles.remove(missile)

    def draw(self, win, camera):
        for missile in self.missiles:
            win.blit(missile.get_image(), camera.apply(missile.position))

    def update(self, dt, plane):
        removals = []
        for missile in self.missiles:
            if missile.active and not missile.been_hit:
                control_missile(missile, plane, dt)
                missile.update(dt, plane)
            else:
                removals.append(missile)

        for missile in removals:
            self.remove(missile)

        return self.hits(plane)

    def spawn_missile(self, plane):

        position = random_vector() * SPAWN_RADIUS + plane.position
        missileToPlane = position - plane.position
        # turn a lil bit
        self.add(Missile(position, missileToPlane))

    def hits(self, plane):
        hit_list = []
        for missile in self.missiles:
            if missile.been_hit:
                continue
            if distance(missile, plane) < 5:
                missile.hit()
                plane.hit()
                hit_list.append(missile.position)

            for other in self.missiles:
                if other.been_hit:
                    continue
                if missile is other:
                    continue
                if distance(missile, other) < 5:
                    hit_list.append(missile.position)

                    missile.hit()
                    other.hit()
        return hit_list

    def get_visable(self, plane):
        visable = []
        for missile in self.missiles:
            dis = distance(missile, plane)
            if dis < PLANE_VISABLE_RANGE:
                visable.append(missile)
            elif dis <= PLANE_VISABLE_RANGE * 1.5:
                p2m = missile.position - plane.position
                if abs(plane.velocity.angle_to(p2m)) < math.pi / 6:
                    visable.append(missile)

        return visable


def control_missile(missile, plane, dt):
    m2p = -missile.position + plane.position

    t = math.atan2(m2p.x, m2p.y)

    if not missile.has_seen_plane:

        missile.heading = t
        missile.target_heading = t

    # missile.target_heading = t
    new_heading, los_angle = missile_guidance(missile, plane, missile.los_angle, dt)
    missile.set_target_heading(new_heading)
    missile.los_angle = los_angle


# CHAT GPT
def angle_wrap(a):
    """Wrap angle to [-pi, pi]."""
    while a > math.pi:
        a -= 2 * math.pi
    while a < -math.pi:
        a += 2 * math.pi
    return a


def signed_angle_diff(a, b):
    """Return the smallest signed difference from b to a in [-pi, pi]."""
    diff = (a - b) % (2 * math.pi)
    if diff > math.pi:
        diff -= 2 * math.pi
    return diff


def missile_guidance(
    missile,
    plane,
    prev_los_angle,  # radians (from previous frame)
    dt,  # time step
    nav_gain=3.0,  # PN gain (typically 3–5)
):
    """
    Returns:
        new_missile_heading,
        current_los_angle
    """

    # --- Relative position ---
    rel = plane.position - missile.position

    # Line-of-sight angle
    los_angle = math.atan2(rel.y, rel.x)

    # LOS rate (angular velocity)
    los_rate = signed_angle_diff(los_angle, prev_los_angle) / dt

    # Proportional Navigation turn command
    turn_rate = nav_gain * los_rate

    # Update missile heading
    new_heading = missile.heading + turn_rate * dt
    new_heading = angle_wrap(new_heading)

    return new_heading, los_angle
