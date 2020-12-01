import pygame
import random
import math
from pygame import mixer


# initialize the pygame
pygame.init()

# make the screen
screen = pygame.display.set_mode((900, 700))

# background
background = pygame.image.load('background.png')


#background sound
mixer.music.load('backgroundmus.wav')
mixer.music.play(-1)




# name of the window and the icon
pygame.display.set_caption("SPACE CHALLENGE")
icon = pygame.image.load('rocket icon.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('space ship.png')
playerX = 420
playerY = 600
playerX_change = 0

# enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):

    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 835))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3.0)
    enemyY_change.append(60)


# bullet
bulletImg = pygame.image.load('fire bullet.png')
bulletX = 0
bulletY = 600
bulletX_change = 0
bulletY_change = 8.0
bullet_state = "ready"


#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',50)
textX = 10
textY = 10


#game over text
over_font = pygame.font.Font('freesansbold.ttf',80)
def show_score(x,y):
    score = font.render("Score : " + str(score_value),True, (255,255,255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render(" GAME OVER ", True, (255, 255, 255))
    screen.blit(over_text, (200 ,350))





def player(x, y):
    screen.blit(playerImg, (x, y))
    # blit means to draw


def enemy(x, y , i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 23, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 20 :
        return True
    else:
        return False


running = True
while running:

    screen.fill((92, 90, 240))

    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if event.type == pygame.KEYDOWN:

        if event.key == pygame.K_LEFT:
            playerX_change = -5.0

        if event.key == pygame.K_RIGHT:
            playerX_change = 5.0

        if event.key == pygame.K_SPACE:
            if bullet_state is "ready":
                bullet_Sound = mixer.Sound('shoot.wav')     #setting the sound of the bullet
                bullet_Sound.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 840:
        playerX = 840


    for i in range(num_of_enemies):


        #game over
        if enemyY[i]>550:
            for j in range(num_of_enemies):                 #game over text
                enemyY[j]= 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 3.0
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 840:
            enemyX_change[i] = -3.0
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('dead.wav')
            explosion_Sound.play()
            bulletY = 600
            bullet_state = "ready"
            score_value += 1
            #print(score)
            enemyX[i] = random.randint(0, 835)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i],i)


    if bulletY <= 0:
        bulletY = 600
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    #collision
    collision = isCollision (enemyX[i],enemyY[i],bulletX,bulletY)
    if collision:
        bulletY = 600
        bullet_state="ready"
        score_value+=1
        #print(score)
        enemyX[i] = random.randint(0, 835)
        enemyY[i] = random.randint(50, 150)

    enemy(enemyX[i] , enemyY[i] , i)

    player(playerX, playerY)  # always use this after the screen fill function not before that
    show_score(textX,textY)
    pygame.display.update()