import pygame
import time
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
CENTER = (WIDTH // 2, HEIGHT // 2)

# Load images
background = pygame.image.load("mickey.png")  # Mickey's face as the clock background
minute_hand = pygame.image.load("hand.png")  # Right hand (minutes)
second_hand = pygame.image.load("hand.png")  # Left hand (seconds)

# Resize images
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
minute_hand = pygame.transform.scale(minute_hand, (200, 20))
second_hand = pygame.transform.scale(second_hand, (200, 20))

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

# Function to rotate and blit hands
def blit_rotate_center(surf, image, angle, pos):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=pos)
    surf.blit(rotated_image, new_rect.topleft)

# Main loop
running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    
    # Get current time
    current_time = time.localtime()
    minutes = current_time.tm_min
    seconds = current_time.tm_sec
    
    # Convert to angles
    minute_angle = -(minutes * 6)  # 360 degrees / 60 minutes
    second_angle = -(seconds * 6)  # 360 degrees / 60 seconds
    
    # Draw hands
    blit_rotate_center(screen, minute_hand, minute_angle, CENTER)
    blit_rotate_center(screen, second_hand, second_angle, CENTER)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    pygame.time.delay(1000)  # Update every second

pygame.quit()
