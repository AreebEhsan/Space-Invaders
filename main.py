import pygame
import random
import math
import time
from pygame import mixer

pygame.init()  # Initializing pygame

screen = pygame.display.set_mode((800, 600))  # creating the screen

background = pygame.image.load("space bg.png")

mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("game-controller.png")
pygame.display.set_icon(icon)

# Event -> Clicking, pressing keys, basically anything happening inside our game window

# Player

player_img = pygame.image.load("spaceship.png")
p1 = 370
p2 = 480
p1_change = 0

# Enemy

enemy_img = []
e1 = []
e2 = []
e1_change = []
e2_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('alien.png'))
    e1.append(random.randint(0, 800))
    e2.append(random.randint(50, 150))
    e1_change.append(4)
    e2_change.append(40)

# Bullet

b_img = pygame.image.load("bullet (1).png")
b1 = 0
b2 = 480
b1_change = 0
b2_change = 30
b_state = "ready"

# Score

score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
score = 0
textX = 10
textY = 10

# Game Over Text

over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text(x, y):
    over_text = over_font.render("GAME OVER " + str(score_val), True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def fire_bullet(x, y):
    global b_state
    b_state = "fire"
    screen.blit(b_img, (x + 16, y + 10))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def isCollision(e1, e2, b1, b2):
    distance = math.sqrt((math.pow(e1 - b1, 2)) + (math.pow(e2 - b2, 2)))
    if distance < 27:

        return True

    else:
        return False


# Game loop
running = True

while running:
    screen.fill((17, 142, 238))  # RGB -> Red, Green, Blue
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Checking the direction of keystroke

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                p1_change = -5
            if event.key == pygame.K_RIGHT:
                p1_change = 5
            if event.key == pygame.K_SPACE:
                if b_state == "ready":
                    bullet_sound = mixer.Sound('shoot.wav')
                    bullet_sound.play()
                    b1 = p1
                    fire_bullet(b1, b2)

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    p1_change = 0

    # Boundary check

    p1 += p1_change

    if p1 <= 0:
        p1 = 0
    elif p1 >= 736:
        p1 = 736
    player(p1, p2)

    # Enemy Movement

    for i in range(num_of_enemies):

        # Game Over

        if e2[i] > 440:
            for j in range(num_of_enemies):
                e2[j] = 2000
            game_over_text(200, 250)
            break

        e1[i] += e1_change[i]

        if e1[i] <= 0:
            e1_change[i] = 4
            e2[i] += e2_change[i]
        elif e1[i] >= 736:
            e1_change[i] = -4
            e2[i] += e2_change[i]

            # Collision
        collision = isCollision(e1[i], e2[i], b1, b2)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            b2 = 480
            b_state = "ready"
            score_val += 1
            print(score)
            e1[i] = random.randint(0, 735)
            e2[i] = random.randint(50, 100)
        enemy(e1[i], e2[i], i)
    # Bullet movement

    if b2 <= 0:
        b2 = 480
        b_state = "ready"

    if b_state == "fire":
        fire_bullet(b1, b2)
        b2 -= b2_change

    player(p1, p2)

    show_score(textX, textY)
    pygame.display.update()
