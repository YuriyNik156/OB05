import pygame
import sys

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_RADIUS = 10
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


# Класс для управления кирпичами
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))


# Класс для управления платформой
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        self.rect.x = max(0, min(SCREEN_WIDTH - PADDLE_WIDTH, self.rect.x))


# Класс для управления мячом
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = [4, -4]

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Столкновение с краями экрана
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.velocity[0] = -self.velocity[0]
        if self.rect.top <= 0:
            self.velocity[1] = -self.velocity[1]

        # Если мяч падает за нижнюю границу
        if self.rect.bottom >= SCREEN_HEIGHT:
            pygame.quit()
            sys.exit()


# Инициализация игры
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arkanoid")
clock = pygame.time.Clock()

# Создание объектов
bricks = pygame.sprite.Group()
for x in range(0, SCREEN_WIDTH, BRICK_WIDTH):
    for y in range(0, 200, BRICK_HEIGHT):
        bricks.add(Brick(x, y))

paddle = Paddle(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

all_sprites = pygame.sprite.Group(paddle, ball, *bricks)

# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Обновление объектов
    all_sprites.update()

    # Проверка столкновений
    if pygame.sprite.collide_rect(ball, paddle):
        ball.velocity[1] = -ball.velocity[1]

    hit_bricks = pygame.sprite.spritecollide(ball, bricks, True)
    if hit_bricks:
        ball.velocity[1] = -ball.velocity[1]

    # Отрисовка объектов
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)