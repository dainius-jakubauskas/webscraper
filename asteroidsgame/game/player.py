import pygame
from circleshape import CircleShape
from shot import Shot
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_SHOOT_SPEED, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS


# Base class for game objects
class Player(CircleShape):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self, dt: float) -> float:
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.rotate(-dt)
            if keys[pygame.K_d]:
                self.rotate(dt)
            if keys[pygame.K_w]:
                self.move(dt)
            if keys[pygame.K_s]:
                self.move(-dt)
            if keys[pygame.K_SPACE]:
                self.shoot()

            self.cooldown_timer -= dt



    def move(self, dt: float) -> float:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector



    def shoot(self):
        if self.cooldown_timer > 0:
            return False
        else:
            shot = Shot(self.position.x, self.position.y)

            unit_vector_shot = pygame.Vector2(0, 1)
            rotated_vector_shot = unit_vector_shot.rotate(self.rotation)
            rotated_with_speed_vector_shot = rotated_vector_shot * PLAYER_SHOOT_SPEED
            shot.velocity = rotated_with_speed_vector_shot
            self.cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
