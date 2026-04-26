import pygame
import sys
from constants import *
from circleshape import CircleShape
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from logger import log_event
from shot import Shot

def get_asteroid_score(radius):
    if radius <= ASTEROID_MIN_RADIUS:
        return SCORE_SMALL_ASTEROID
    if radius <= ASTEROID_MIN_RADIUS * 2:
        return SCORE_MEDIUM_ASTEROID
    return SCORE_LARGE_ASTEROID

def main():
    from logger import log_state

    pygame.init()

    clock = pygame.time.Clock()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Shot.containers = (shots, drawable, updatable)
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)

    dt = 0
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    score = 0

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH }")
    print(f"Screen height: {SCREEN_HEIGHT }")

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        updatable.update(dt)
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            for shot in shots:
                if shot.collides_with(asteroid):
                    score += get_asteroid_score(asteroid.radius)
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                    break
        screen.fill(0)
        for entity in drawable:
            entity.draw(screen)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"score: {score}", True, "white")
        screen.blit(score_text,(20, 20))
        pygame.display.flip()

        dt = clock.tick(60)/1000

if __name__ == "__main__":
    main()
