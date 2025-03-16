# Импортирование библиотеки pyGame и random
import pygame
import random

pygame.init() # Инициализируем pygame

# Размер окна
HEIGHT, WIDTH = 600, 400 # Высота и ширина игрового окна
SCREEN = pygame.display.set_mode(HEIGHT, WIDTH) # Отображение на экране
pygame.display.set_caption("Гонки") # Название окна

# Создание цветов
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Создаение класса игрока
class Player():
    def __init__(self):
        self.height, self.width = 60, 40 # Размер гоночной машины игрока
        self.x = WIDTH // 2 - self.width // 2 # Положение гоночной машины по оси x
        self.y = HEIGHT - self.height - 10 # Положение гоночной машины по оси y
        self.speed = 5 # Скорость движения машины игрока

    def move(self, direction):
        if direction == "LEFT" and self.x > 0:
            self.x -= self.speed # Перемещение машины игрока влево при нажатии "LEFT"
        if direction == "RIGHT" and self.x < WIDTH - self.width:
            self.x += self.speed # Перемещение машины игрока вправо при нажатии "RIGHT"

    def draw(self):
        pygame.draw.rect(SCREEN, BLUE, (self.x, self.y, self.height, self.width)) # Отрисовка машины игрока

# Создание класса препятствия
class Obstacle():
    def __init__(self):
        self.height, self.width = 60, 40 # Размер машин-препятствий
        self.x = random.randint(0, WIDTH - self.width) # Случайное расположение препятствий по оси x
        self.y = -self.height # Появление препятствий на оси y
        self.speed = 5 # Скорость перемещения машин-препятствий

    def move(self):
        self.y += self.speed # Перемещение машин-препятствий по оси y

    def draw(self):
        pygame.draw.rect(SCREEN, RED, (self.x, self.y, self.height, self.width))  # Отрисовка машин-препятствий

# Создание основной функции игры
