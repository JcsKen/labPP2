import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
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
food = (random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE))
score = 0
level = 1
speed = 10

# Function to generate food at a valid position
def generate_food():
    while True:
        new_food = (random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE))
        if new_food not in snake:
            return new_food

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
        score += 1
        food = generate_food()
        # Level up every 3 points
        if score % 3 == 0:
            level += 1
            speed += 2  # Increase speed
    else:
        snake.pop()  # Remove tail if no food eaten
    
    # Draw food
    pygame.draw.rect(screen, FOOD_COLOR, (*food, GRID_SIZE, GRID_SIZE))
    
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