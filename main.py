import pygame
from pygame.math import Vector2
import random

# wlaczenie pygame (bez tego gowno n dziala)
pygame.init()

# ustawienia mapy
cell_size = 20
grid_size = 25
screen_size = cell_size * grid_size

# kolory
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# pojawienie ekranu i zegara, bez zegara waz spierdala
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Snejk juanito")
clock = pygame.time.Clock()

class Snake: #gracz
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)

    def draw(self): #pojawienie weza na mapie
        for segment in self.body:
            segment_rect = pygame.Rect(segment.x * cell_size, segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, BLUE, segment_rect)

    def update(self): #pozwala na updatowanie pozycji i ruch
        self.body = self.body[:-1]
        new_head = self.body[0] + self.direction

        # jak waz zajebie z dynki w bande to wychodzi z drugiej strony
        if new_head.x < 0:
            new_head.x = grid_size - 1
        elif new_head.x >= grid_size:
            new_head.x = 0
        if new_head.y < 0:
            new_head.y = grid_size - 1
        elif new_head.y >= grid_size:
            new_head.y = 0

        self.body.insert(0, new_head)

class Food: #pozywienie dla gracza
    def __init__(self, snake_body):
        self.position = self.random_position(snake_body)

    def draw(self): #pojawienie pozywienia
        food_rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, RED, food_rect)

    def random_cell(self): #random ahh pozycja jedzenia
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        return Vector2(x, y)

    def random_position(self, snake_body): #teleportacja jedzenia w inne miejsce jak gracz zje
        position = self.random_cell()
        while position in snake_body:
            position = self.random_cell()
        return position

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)

    def draw(self):
        self.snake.draw()
        self.food.draw()

    def update(self):
        self.snake.update()

    def check_collision(self):
        if self.snake.body[0] == self.food.position:
            self.snake.body.append(self.snake.body[-1])  # powieksza weza
            self.food.position = self.food.random_position(self.snake.body)

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)

game = Game()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # sterowanie gierka
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if game.snake.direction != Vector2(1, 0):
                    game.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT:
                if game.snake.direction != Vector2(-1, 0):
                    game.snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_UP:
                if game.snake.direction != Vector2(0, 1):
                    game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN:
                if game.snake.direction != Vector2(0, -1):
                    game.snake.direction = Vector2(0, 1)

        # updejtowanie weza (co 200 milisekund rn)
        if event.type == SNAKE_UPDATE:
            game.update()
            game.check_collision()

    screen.fill(WHITE)
    game.draw()
    pygame.display.update()
    clock.tick(60) #60 fps a ludzkie oko i tak widzi tylko 30

pygame.quit()
