import pygame
from logger import log_event
import random
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            LINE_WIDTH
        )


    def update(self, dt):
        self.position += self.velocity*dt
        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)


    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        new_radius = self.radius / 2

        base_velocity = self.velocity

        angle = random.uniform(20,50)
        vel1 = base_velocity.rotate(angle) * 1.12
        vel2 = base_velocity.rotate(-angle) * 1.12

        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = vel1

        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = vel2