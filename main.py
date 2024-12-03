import pygame
import random
import math
from pygame import mixer

#initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load('background.png')

#background music
mixer.music.load('sounds/background.wav')
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
  enemyImg.append(pygame.image.load('enemy.png'))
  enemyX.append(random.randint(0,735))
  enemyY.append(random.randint(50,150))
  enemyX_change.append(1)
  enemyY_change.append(40)


#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#sore
score_value = 0
font = pygame.font.Font('fonts/PressStart2P-Regular.ttf',24)

textX = 10
textY = 10

#game over
over_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf',64)

def show_score(x,y):
  score = font.render("Score: " + str(score_value),True,(0,128,0))
  screen.blit(score,(x,y))

def game_over_text():
    # Show game over text
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    over_text_rect = over_text.get_rect(center=(800 // 2, 250))
    screen.blit(over_text, over_text_rect)
    
    # show restart text
    restart_text = font.render("Press Enter to Restart", True, (255, 255, 255))
    restart_text_rect = restart_text.get_rect(center=(800 // 2, 350))
    screen.blit(restart_text, restart_text_rect)
    pygame.display.update()

def player(x,y):
  screen.blit(playerImg,(x,y))

def enemy(x,y,i):
  screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
  global bullet_state
  bullet_state = "fire"
  screen.blit(bulletImg,(x+16,y+10))

def is_collision(enemyX,enemyY,bulletX,bulletY):
  distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
  if distance < 27:
    return True
  else:
    return False

def reset_game():
    global playerX, playerY, playerX_change, bulletX, bulletY, bullet_state, score_value, enemyX, enemyY, enemyX_change, enemyY_change, game_over
    playerX = 370
    playerY = 480
    playerX_change = 0
    bulletX = 0
    bulletY = 480
    bullet_state = "ready"
    score_value = 0
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(50, 150)
        enemyX_change[i] = 1
        enemyY_change[i] = 40
    game_over = False
    mixer.music.play(-1)

#Game Loop
running = True
game_over = False
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over:
            # Esperar una tecla para reiniciar
            if event.type == pygame.KEYDOWN:
                reset_game()
            continue

        # Si no hay game over, procesar controles
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    mixer.Sound('sounds/laser.wav').play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if not game_over:
        #player movement
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        #enemy movement
        for i in range(num_of_enemies):
            #game over
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over = True
                mixer.music.stop()  # Detener música al perder
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 1
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -1
                enemyY[i] += enemyY_change[i]

            #collision
            collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                mixer.Sound('sounds/explosion.wav').play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        #bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)
    
        pygame.display.update()
