import pygame, sys
from pygame.locals import *
import random, time

# Initialize pygame
pygame.init()

# Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

# Defining Colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SPEED = 3
COINS_COLLECTED = 0
COIN_WEIGHT_THRESHOLDS = [1, 2, 3]  # Different coin values
SPEED_INCREASE_THRESHOLD = 10  # Increase enemy speed after collecting N coins

# Load Assets
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
background = pygame.image.load("AnimatedStreet.png")
coin_img = pygame.image.load("Coin.png")
coin_img = pygame.transform.scale(coin_img, (15, 15))

# Create display window
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racing Game")

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy (1).png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player (1).png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Coin Class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.value = random.choice(COIN_WEIGHT_THRESHOLDS)  # Assign random weight

    def move(self):
        self.rect.move_ip(0, COIN_SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Initialize Sprites
P1 = Player()
E1 = Enemy()
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1)

# Generate initial coins
for _ in range(5):
    coin = Coin()
    coins.add(coin)
    all_sprites.add(coin)

# Speed Increase Event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Render Background
    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    coins_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 100, 10))

    # Move and Draw Sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
        if isinstance(entity, Coin):
            coin_value_text = font_small.render(str(entity.value), True, BLACK)
            DISPLAYSURF.blit(coin_value_text, (entity.rect.x + 5, entity.rect.y - 10))

    # Check Coin Collection
    collected_coins = pygame.sprite.spritecollide(P1, coins, True)
    for coin in collected_coins:
        COINS_COLLECTED += coin.value
        new_coin = Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)

    # Increase enemy speed when collecting N coins
    if COINS_COLLECTED >= SPEED_INCREASE_THRESHOLD:
        SPEED += 1
        COINS_COLLECTED = 0  # Reset threshold counter

    # Check for Collision with Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()
    
    pygame.display.update()
    FramePerSec.tick(FPS)
