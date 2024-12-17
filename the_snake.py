from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 6

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


class GameObject:
    """Родительский класс для всех объектов."""

    def __init__(self):
        """Инициализация базового игрового объекта."""
        self.position = CENTER_POSITION
        self.body_color = (0, 0, 0)

    def draw(self):
        """Отрисовка игрового объекта."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        """Инициализация яблока."""
        super().__init__()
        self.body_color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Случайным образом изменяет позицию яблока на поле."""
        new_position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
        self.position = new_position

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self, apple=None):
        """Метод инициализация змейки."""
        if apple is None:
            apple = Apple()
        super().__init__()
        self.apple_link = apple
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [CENTER_POSITION]
        self.body_color = (0, 255, 0)
        self.last = None

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод для смены направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для движения и подбирания яблока."""
        next_distance_move = (
            GRID_SIZE * self.direction[0],
            GRID_SIZE * self.direction[1],
        )
        current_head_position = self.get_head_position()
        new_head_position = [
            current_head_position[0] + next_distance_move[0],
            current_head_position[1] + next_distance_move[1],
        ]

        # Обработка выхода за границы
        if SCREEN_WIDTH <= new_head_position[0]:
            new_head_position[0] = 0 + SCREEN_WIDTH - new_head_position[0]
        elif new_head_position[0] < 0:
            new_head_position[0] = SCREEN_WIDTH - abs(new_head_position[0])

        if SCREEN_HEIGHT <= new_head_position[1]:
            new_head_position[1] = 0 + SCREEN_HEIGHT - new_head_position[1]
        elif new_head_position[1] < 0:
            new_head_position[1] = SCREEN_HEIGHT - abs(new_head_position[1])

        new_head_position = tuple(new_head_position)

        # Врезание в самого себя
        if new_head_position in self.positions[2:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            self.apple_link.randomize_position()
            self.reset()
            return

        # Подбор яблока
        if new_head_position != self.apple_link.position:
            self.last = self.positions.pop()
        else:
            self.apple_link.randomize_position()

        self.positions.insert(0, new_head_position)
        self.length = len(self.positions)

    def get_head_position(self):
        """Метод для получения координат головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает параметры змейки к начальному состоянию."""
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [CENTER_POSITION]


def handle_keys(game_object):
    """Метод для реакции на нажатие стрелочек."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главный метод."""
    pygame.init()
    apple = Apple()
    snake = Snake(apple)

    while True:
        snake.draw()
        apple.draw()
        pygame.display.update()

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
