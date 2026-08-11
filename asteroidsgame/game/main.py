import pygame
import sys
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from constants import *
from logger import log_state, log_event



def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()

    clock = pygame.time.Clock()
    dt = 0.0

    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)


    player = Player(x, y)
    asteroidfield = AsteroidField()


    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



    #### Game loop

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    return

        updatable.update(dt) ##update values

        for item in asteroids:    ##collision-with-player check
            if item.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        for item in asteroids:    ##collision-with-shot check
            for shot in shots:
                if shot.collides_with(item):
                    log_event("asteroid_shot")
                    item.split()





        screen.fill("black") ##make screen

        for thing in drawable:  ##drawing items
            thing.draw(screen)

        pygame.display.flip() ##rendering, everything becomes visible at the screen

        dt = clock.tick(60)/1000





if __name__ == "__main__":
    main()
