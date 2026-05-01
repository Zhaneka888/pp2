# ============================================================
# IMPORTS
# ============================================================
import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

# FPS
FPS = 60
FramePerSec = pygame.time.Clock()

#COLORS

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD  = (255, 215, 0)   # gold coin
SILVER = (192,192,192)  # silver coin
BRONZE = (205,127,50)   # bronze coin

#SCREEN

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600
SPEED         = 5       
SCORE         = 0       
SPEED_INCREASE_THRESHOLD = 5

font       = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over  = font.render("Game Over", True, BLACK)

#background initialization
background = pygame.image.load("AnimatedStreet.png")


DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


#Enemy class,spawns enemies randomly
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect  = self.image.get_rect()
        #Spawning enemies randomly
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        #Moving enemies
        self.rect.move_ip(0, SPEED)

        #Sending enemy back to the random position at the top
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


#Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect  = self.image.get_rect()
        #Spawning player
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        #Moving left(A key)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        # Moving right(D key)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


#Coins class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #Generates random type of coins
        #The more the coins weighs - the more player gets
        self.weight = random.choice([1, 2, 3])

        #Counting value of a coin based on weight
        size = 10 + self.weight * 8

        # Creating the surface for the coins
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)

        #Coins weight and color relationship
        if self.weight == 1:
            color = GOLD    # Gold — 1 pts
        elif self.weight == 2:
            color = SILVER  # Silver — 2 pts
        else:
            color = BRONZE  # Bronze — 3 pts

        # Creating the coins
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)

        self.rect = self.image.get_rect()
        # Setting random position for the coin
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        #Coin speed
        self.rect.move_ip(0, SPEED)

        #Deleting the coin if its out of the bounds
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


#Initializing sprites for player and enemies
P1 = Player()
E1 = Enemy()

#Enemies group for checking bumps with player
enemies = pygame.sprite.Group()
enemies.add(E1)

#Group for checking if the coin has been picked up
coins = pygame.sprite.Group()

#Group of all of the sprites, required to track the motion
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#Speed increasing event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#Coin generation event(every 1.5 seconds)
SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_COIN, 1500)

#Game loop
while True:
    for event in pygame.event.get():

        #Inreasing the speed
        if event.type == INC_SPEED:
            SPEED += 0.5

        #Coin generation
        if event.type == SPAWN_COIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

        #Leaving the game
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #bg
    DISPLAYSURF.blit(background, (0, 0))

    #Score
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    #Sprite stuff
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    #Checking for gathered coins
    collected = pygame.sprite.spritecollide(P1, coins, True)
    for coin in collected:
        #Adding scores
        SCORE += coin.weight

        #Incrementing the speed of the enemies
        if SCORE % SPEED_INCREASE_THRESHOLD == 0:
            SPEED += 1
            print(f"Скорость увеличена! SPEED = {SPEED}, SCORE = {SCORE}")

    #Checking for accidents
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        #Game over screen
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()

        #Removing all entiies and sprites
        for entity in all_sprites:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    #Updating the frames
    pygame.display.update()
    FramePerSec.tick(FPS)