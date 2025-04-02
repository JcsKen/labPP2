import pygame
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
SNAKE_COLOR = (0, 255, 0)
FOOD_COLORS = {1: (255, 0, 0), 2: (255, 165, 0), 3: (255, 255, 0)}  # Different colors for food values
BG_COLOR = (0, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Snake initialization
snake = [(WIDTH // 2, HEIGHT // 2)]
direction = RIGHT
score = 0
level = 1
speed = 10

# Food properties
food = None
food_weight = None
food_spawn_time = None
FOOD_LIFETIME = 5000  # Food disappears after 5 seconds

# Function to generate food with random weight and timer
def generate_food():
    global food_weight, food_spawn_time
    while True:
        new_food = (random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE))
        if new_food not in snake:
            food_weight = random.choice([1, 2, 3])  # Random food weight
            food_spawn_time = pygame.time.get_ticks()  # Record spawn time
            return new_food

# Generate first food
food = generate_food()

# Main game loop
running = True
while running:
    screen.fill(BG_COLOR)
    
    # Event handling
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
    
    # Move the snake
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0] * GRID_SIZE, head_y + direction[1] * GRID_SIZE)
    
    # Check for wall collision
    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        running = False
        continue
    
    # Check for self-collision
    if new_head in snake:
        running = False
        continue
    
    # Add new head to the snake
    snake.insert(0, new_head)
    
    # Check if food is eaten
    if new_head == food:
        score += food_weight
        food = generate_food()
        # Level up every 3 points
        if score % 3 == 0:
            level += 1
            speed += 2  # Increase speed
    else:
        snake.pop()  # Remove tail if no food eaten
    
    # Check if food has expired
    if pygame.time.get_ticks() - food_spawn_time > FOOD_LIFETIME:
        food = generate_food()
    
    # Draw food with its respective color based on weight
    pygame.draw.rect(screen, FOOD_COLORS[food_weight], (*food, GRID_SIZE, GRID_SIZE))
    
    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, (*segment, GRID_SIZE, GRID_SIZE))
    
    # Display score and level
    font = pygame.font.Font(None, 24)
    score_text = font.render(f"Score: {score}  Level: {level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
