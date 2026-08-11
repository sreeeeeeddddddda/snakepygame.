import pygame
import sys
import random

# 1. Initialize Pygame
pygame.init()

# 2. Setup Display
WIDTH, HEIGHT = 600, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Snake Game")

# 3. Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 4. Settings & Fonts
clock = pygame.time.Clock()
SNAKE_SIZE = 20
FPS = 10

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 30)

def draw_score(score):
    value = score_font.render("Score: " + str(score), True, WHITE)
    window.blit(value, [10, 10])

def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(window, GREEN, [segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE])

def display_message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(WIDTH / 2, HEIGHT / 2 + y_offset))
    window.blit(mesg, text_rect)

def game_loop():
    game_over = False
    game_close = False

    # Snake head position
    x1 = WIDTH // 2
    y1 = HEIGHT // 2

    # Movement variables
    x1_change = 0
    y1_change = 0

    # Body mechanics
    snake_list = []
    length_of_snake = 1

    # Food placement
    foodx = round(random.randrange(0, WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
    foody = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE

    while not game_over:

        # --- GAME OVER MENU ---
        while game_close:
            window.fill(BLACK)
            display_message("Game Over!", RED, -30)
            display_message("Press C to Play Again or Q to Quit", WHITE, 10)
            draw_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_close = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_SIZE
                    x1_change = 0

        # --- BOUNDARY COLLISION ---
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        # --- UPDATE BODY ---
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # --- SELF COLLISION ---
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # --- RENDER GRAPHICS ---
        window.fill(BLACK)
        pygame.draw.rect(window, RED, [foodx, foody, SNAKE_SIZE, SNAKE_SIZE])
        draw_snake(snake_list)
        draw_score(length_of_snake - 1)
        pygame.display.update()

        # --- EAT FOOD ---
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            foody = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            length_of_snake += 1

        # Control speed (increases as score goes up)
        clock.tick(FPS + (length_of_snake // 3))

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()