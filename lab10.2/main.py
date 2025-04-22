import pygame
import random
from db import connect_db, get_or_create_user, get_last_score, save_game_state
from levels import get_speed_for_level, get_walls_for_level

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
SNAKE_COLOR = (0, 255, 0)
FOOD_COLORS = {1: (255, 0, 0), 2: (255, 165, 0), 3: (255, 255, 0)}
BG_COLOR = (0, 0, 0)
FOOD_LIFETIME = 5000

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def generate_food(snake, walls):
    while True:
        food = (random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE))
        if food not in snake and food not in walls:
            weight = random.choice([1, 2, 3])
            return food, weight, pygame.time.get_ticks()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # DATABASE SETUP
    conn, cur = connect_db()
    username = input("Enter your username: ")
    user_id = get_or_create_user(cur, conn, username)
    last = get_last_score(cur, user_id)
    score, level = last if last else (0, 1)

    # GAME INITIALIZATION
    speed = get_speed_for_level(level)
    walls = get_walls_for_level(level)
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = RIGHT
    food, food_weight, food_spawn_time = generate_food(snake, walls)
    paused = False
    running = True

    # GAME LOOP
    while running:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_s and paused:
                    save_game_state(cur, conn, user_id, score, level)
                    print("Game saved.")
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if paused:
            pygame.display.flip()
            clock.tick(5)
            continue

        head_x, head_y = snake[0]
        new_head = (head_x + direction[0] * GRID_SIZE, head_y + direction[1] * GRID_SIZE)

        # COLLISION DETECTION
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake or
            new_head in walls):
            print("Game Over!")
            break

        snake.insert(0, new_head)

        if new_head == food:
            score += food_weight
            if score % 3 == 0:
                level += 1
                speed = get_speed_for_level(level)
                walls = get_walls_for_level(level)
            food, food_weight, food_spawn_time = generate_food(snake, walls)
        else:
            snake.pop()

        if pygame.time.get_ticks() - food_spawn_time > FOOD_LIFETIME:
            food, food_weight, food_spawn_time = generate_food(snake, walls)

        pygame.draw.rect(screen, FOOD_COLORS[food_weight], (*food, GRID_SIZE, GRID_SIZE))
        for segment in snake:
            pygame.draw.rect(screen, SNAKE_COLOR, (*segment, GRID_SIZE, GRID_SIZE))
        for wall in walls:
            pygame.draw.rect(screen, (100, 100, 100), (*wall, GRID_SIZE, GRID_SIZE))

        font = pygame.font.Font(None, 24)
        text = font.render(f"Score: {score}  Level: {level}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(speed)

    # SAVE GAME ON EXIT
    save_game_state(cur, conn, user_id, score, level)
    pygame.quit()
    print("Game exited. Progress saved.")


if __name__ == "__main__":
    main()
