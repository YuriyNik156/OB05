# Импорт модулей pygame и random
import pygame
import random

pygame.init() # Инициализация pygame

# Размер окна
WIDTH, HEIGHT = 600, 800 # Ширина и высота экрана
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT)) # Создание окна игры с заданными параметрами
pygame.display.set_caption("Гонки") # Название экрана

# Цвета
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Полосы движения
LANE_WIDTH = WIDTH // 2 # Две полосы движения для машины, каждая из которых занимает половину ширины экрана
LANES = [LANE_WIDTH // 2 + 40, LANE_WIDTH + LANE_WIDTH // 2 - 100] # Координаты для каждой из полос

# Шрифт
font = pygame.font.Font(None, 36) # Стандартный шрифт, размер 36

def draw_text(text, x, y, color = BLACK): # Отрисовка текста (текст, координаты и цвет)
    text_surface = font.render(text, True, color) # Создание изображения текста
    SCREEN.blit(text_surface, (x, y)) # Размещение текста на экране

# Функция для отрисовки машины в виде многоугольника
def draw_car(x, y, color): # Заданы координаты верхней части машины и цвет машины
    pygame.draw.polygon(SCREEN, color, [(x, y + 10), (x + 30, y), (x + 60, y + 10),
                                         (x + 50, y + 80), (x + 10, y + 80)]) # Заданы вершины многоугольника машины
    pygame.draw.rect(SCREEN, BLACK, (x + 10, y + 30, 40, 30)) # Прямоугольник кузова автомобиля

# Экран проигрыша
def game_over(score):
    while True: # Бесконечный цикл
        SCREEN.fill(WHITE) # Очистка экрана и белая заливка
        draw_text("Вы проиграли!", WIDTH // 2 - 80, HEIGHT // 4)
        draw_text(f"Ваш счет: {score}", WIDTH // 2 - 80, HEIGHT // 2)
        draw_text("Нажмите Enter, чтобы начать заново", WIDTH // 2 - 180, HEIGHT // 2 + 50)
        pygame.display.flip() # Обновление экрана для отображения изменений

        for event in pygame.event.get(): # Перебор событий в игре
            if event.type == pygame.QUIT: # Проверка условия закрытия окна
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN: # Проверка условия нажатия любой клавиши
                if event.key == pygame.K_RETURN: # Проверка условия нажатия клавиши Enter
                    main()
                    return

# Главное меню
def main_menu():
    while True: # Бесконечный цикл
        SCREEN.fill(WHITE) # Очистка экрана и белая заливка
        draw_text("Гонки", WIDTH // 2 - 40, HEIGHT // 4)
        draw_text("Нажмите Enter, чтобы начать", WIDTH // 2 - 140, HEIGHT // 2)
        draw_text("Правила: уклоняйтесь от машин!", WIDTH // 2 - 140, HEIGHT // 2 + 50)
        pygame.display.flip() # Обновление экрана для отображения изменений

        for event in pygame.event.get(): # Перебор событий в игре
            if event.type == pygame.QUIT: # Проверка условия закрытия окна
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN: # Проверка условия нажатия любой клавиши
                if event.key == pygame.K_RETURN: # Проверка условия нажатия клавиши Enter
                    main()
                    return

# Класс игрока
class Player:
    def __init__(self):
        self.width, self.height = 60, 90 # Размеры машины игрока
        self.lane = 0  # Начальная полоса (левая)
        self.x = LANES[self.lane] # Установка координаты x в зависимости от полосы
        self.y = HEIGHT - self.height - 10 # Установка координаты y внизу экрана

    def move(self, direction):
        if direction == "LEFT" and self.lane > 0: # Изменение полосы при нажатии LEFT
            self.lane -= 1
        elif direction == "RIGHT" and self.lane < 1: # Изменение полосы при нажатии RIGHT
            self.lane += 1
        self.x = LANES[self.lane] # Обновление позиции машины

    def draw(self):
        draw_car(self.x, self.y, BLUE) # Отрисовка машины игрока (текущие координаты и цвет)

# Класс препятствия
class Obstacle:
    def __init__(self, speed):
        self.width, self.height = 60, 90 # Размеры машин-препятствий
        self.lane = random.choice([0, 1]) # Случайное расположение препятствий на одной из линий
        self.x = LANES[self.lane] # Установка координаты x в зависимости от полосы
        self.y = -self.height # Установка координаты y вверху экрана
        self.speed = speed # Скорость движения препятствий задается переменной speed

    def move(self):
        self.y += self.speed # Движение препятствий вниз по экрану

    def draw(self):
        draw_car(self.x, self.y, RED) # Отрисовка машин-препятствий (текущие координаты и цвет)

# Основная функция игры
def main():
    clock = pygame.time.Clock() # Управление скоростью обновления игры (FPS)
    running = True # Управление основным игровым циклом
    player = Player() # Объект класса Player(), машина игрока
    obstacles = [Obstacle(2)] # Список препятствий с начальной скоростью 2
    score = 0 # Переменная для хранения игрового счета
    speed = 2  # Начальная скорость

    while running: # Бесконечный цикл
        SCREEN.fill(WHITE) # Заполнение экрана белым цветом
        for event in pygame.event.get(): # Перебор событий в игре
            if event.type == pygame.QUIT: # Завершение игры при закрытии окна
                pygame.quit()
                return

        keys = pygame.key.get_pressed() # Получение состояний клавиш на клавиатуре
        if keys[pygame.K_LEFT]: # Перемещение машины игрока влево LEFT
            player.move("LEFT")
        if keys[pygame.K_RIGHT]: # Перемещение машины игрока вправо RIGHT
            player.move("RIGHT")

        # Увеличение скорости со временем
        speed += 0.005

        # Обновление препятствий
        for obstacle in obstacles: # Итерация машин-препятствий
            obstacle.move() # Перемещение машин-препятствий сверху вниз
            if obstacle.y > HEIGHT:
                obstacles.remove(obstacle) # Удаление пройденных препятствий
                obstacles.append(Obstacle(speed)) # Добавление новых препятствий
                score += 1

            # Проверка столкновений игрока с препятствиями
            if (player.x < obstacle.x + obstacle.width and
                    player.x + player.width > obstacle.x and
                    player.y < obstacle.y + obstacle.height and
                    player.y + player.height > obstacle.y):
                game_over(score)
                return

        # Отрисовка объектов
        player.draw() # Отрисовка машины игрока
        for obstacle in obstacles:
            obstacle.draw() # Отрисовка машин-препятствий

        # Отображение счета
        draw_text(f"Score: {score}", 10, 10)

        pygame.display.flip() # Обновление экрана
        clock.tick(30) # Частота кадров (30 в сек.)

if __name__ == "__main__": # Запуск игры
    main_menu()