import pygame
from pygame import mixer
import random
import math

# initialize pygame
pygame.init()

# create the screen
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))

# background image
background = pygame.image.load("background.png")

# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("outer-space-alien.png")
pygame.display.set_icon(icon)

# player icon
playerImg = pygame.image.load("player.png")
playerWidth = playerImg.get_width()
playerHeight = playerImg.get_height()
playerX = screenWidth / 2 - playerWidth / 2
playerY = screenHeight * 0.8
playerX_change = 0

# enemy icon
enemyImg = []
enemyWidth = []
enemyHeight = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyWidth.append(enemyImg[i].get_width())
    enemyHeight.append(enemyImg[i].get_height())
    enemyX.append(random.randint(0, screenWidth - enemyWidth[i]))
    enemyY.append(random.randint(0, int(screenHeight / 4)))
    enemyX_change.append(1)
    enemyY_change.append(enemyHeight[i] / 2)

# bullet
bulletImg = pygame.image.load("bullet.png")
bulletWidth = bulletImg.get_width()
bulletX = 0
bulletY = playerY
bulletY_change = 20  # adjust this value for faster/slower laser speed
# ready = can't see bullet
# fire = bullet is moving
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font("infinite_darkness.ttf", 32)
textX = 10
textY = 10

over_font = pygame.font.Font("infinite_darkness.ttf", 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    text_width = over_text.get_width()
    text_height = over_text.get_height()
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, n):
    screen.blit(enemyImg[n], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + (playerWidth - bulletWidth) / 2, y + 10))


def is_collision(x2, x1, y2, y1):
    # use distance formula
    distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    if distance < 27:
        return True
    else:
        return False


# background position
background1_y = 0
background2_y = -screenHeight

# main game loop
# infinite loop so that the game runs until the user quits
# anything persistent will be in the for loop
running = True
while running:
    # RGB background
    # screen.fill((0, 128, 128))
    # display background image
    screen.blit(background, (0, 0))
    # Scroll the background images
    background1_y += 1  # Adjust the scrolling speed as needed
    background2_y += 1  # Adjust the scrolling speed as needed

    # Reset background position when it goes beyond the screen height
    if background1_y >= screenHeight:
        background1_y = -screenHeight

    if background2_y >= screenHeight:
        background2_y = -screenHeight

    # Draw background images
    screen.blit(background, (0, background1_y))
    screen.blit(background, (0, background2_y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # keystroke check
        if event.type == pygame.KEYDOWN:  # adjust these values for faster/slower player movement
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # player movement
    playerX += playerX_change
    # player boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= screenWidth - playerWidth:
        playerX = screenWidth - playerWidth
    # enemy movement
    for i in range(num_of_enemies):
        # game over when an enemy reaches the bottom
        if enemyY[i] > screenHeight:
            game_over_text()
            pygame.display.update()
            break

        enemyY[i] += 0.7  # adjust this value for faster/slower enemy movement
        # collision detection with player
        collision_player = is_collision(playerX, enemyX[i], playerY, enemyY[i])
        if collision_player:
            game_over_text()
            pygame.display.update()
            running = False
        # collision detection with bullet
        collision_bullet = is_collision(enemyX[i], bulletX, enemyY[i], bulletY)
        if collision_bullet:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, screenWidth - enemyWidth[i])
            enemyY[i] = 0 - enemyHeight[i]
        # display enemy icons
        enemy(enemyX[i], enemyY[i], i)
    # bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"

    # display player icon
    player(playerX, playerY)
    # display score
    show_score(textX, textY)

    pygame.display.update()
