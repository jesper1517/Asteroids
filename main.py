import pygame
import sys

from constants import *
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from logger import log_event, log_state
from shot import Shot

def get_asteroid_score(radius):
    if radius <= ASTEROID_MIN_RADIUS:
        return SCORE_SMALL_ASTEROID
    if radius <= ASTEROID_MIN_RADIUS * 2:
        return SCORE_MEDIUM_ASTEROID
    return SCORE_LARGE_ASTEROID

def reset_game(player, asteroids, shots):
    player.position.x = SCREEN_WIDTH/2
    player.position.y = SCREEN_HEIGHT/2
    player.velocity.x = 0
    player.velocity.y = 0
    player.rotation = 0

    for asteroid in asteroids.copy():
        asteroid.kill()
    for shot in shots.copy():
        shot.kill()

def draw_game_over(screen, score):
    title_font = pygame.font.Font(None,96)
    info_font = pygame.font.Font(None, 42)

    title_text = title_font.render("GAME OVER", True, "white")
    score_text = info_font.render(f"Score: {score}", True, "white")
    restart_text = info_font.render("Tryck R för att spela igen", True, "white")
    quit_text = info_font.render("Tryck ESC för att avsluta", True, "white")

    screen.blit(
        title_text,
        (
            SCREEN_WIDTH / 2 - title_text.get_width() /2,
            SCREEN_HEIGHT / 2 - 120,
        ),
    )

    screen.blit(
        score_text,
        (
            SCREEN_WIDTH / 2 - restart_text.get_width() /2,
            SCREEN_HEIGHT / 2 - 40,
        ),
    )
    
    screen.blit(
        restart_text,(
            SCREEN_WIDTH / 2 - restart_text.get_width() /2,
            SCREEN_HEIGHT /2 + 20,
        ),
    )
    
    screen.blit(
        quit_text,
        (
            SCREEN_WIDTH / 2 - quit_text.get_width() /2,
            SCREEN_HEIGHT /2 + 70,
        ),
    )

def main():
    pygame.init()

    running = True
    score = 0
    game_over = False

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    hud_font = pygame.font.Font(None, 36)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Shot.containers = (shots, drawable, updatable)
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    dt = 0

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH }")
    print(f"Screen height: {SCREEN_HEIGHT }")

    while running:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_r and game_over:
                    score = 0
                    game_over = False
                    reset_game(player, asteroids, shots)

        if not game_over:
            updatable.update(dt)

            for asteroid in asteroids.copy():
                if player.collides_with(asteroid):
                    log_event("player_hit")
                    game_over = True
                    break

                for shot in shots.copy():
                    if shot.collides_with(asteroid):
                        score += get_asteroid_score(asteroid.radius)
                        log_event("asteroid_shot")
                        shot.kill()
                        asteroid.split()

                        break
        screen.fill(0)

        for entity in drawable:
            entity.draw(screen)

        score_text = hud_font.render(f"score: {score}", True, "white")
        screen.blit(score_text,(20, 20))

        if game_over:
            draw_game_over(screen, score)

        pygame.display.flip()

        dt = clock.tick(60)/1000

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
