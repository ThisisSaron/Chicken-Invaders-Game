import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((1536,810))

pygame.display.set_caption("Chicken Invaders ")
icon = pygame.image.load("redchicken.JPEG")
pygame.display.set_icon(icon)

level = 0
display = 0
runningmain = True
while runningmain:
    if display == 0:
        level = 0
        background = pygame.image.load("intro.png")
        intro_sound = mixer.Sound("intro.mp3")
        intro_sound.play()
        running2 = True
        while running2:
            screen.fill((0,0,0))
            screen.blit(background,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running2 = False
                    runningmain = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    display = 2
                    intro_sound.stop()
                    running2 = False
            pygame.display.update()
    if display == 2:
        #initialize screen and background
        background = pygame.image.load("bg2.png")

        rooster_sound = mixer.Sound("rooster.wav")
        rooster_sound.play()

        mixer.music.load("background.wav")
        mixer.music.play(-1)

        base_font = pygame.font.Font("freesansbold.ttf",36)
        #spaceship initial load
        spaceship = pygame.image.load("spaceship.png")
        shipx = 768
        shipy = 700
        changex = 0
        changey = 0

        #enemies initial load
        enemyimg = []
        enemyX=[]
        enemyY=[]
        enemyX_change = []
        enemyY_change=[]
        
        eggimg = []
        egg_state = []
        eggX=[]
        eggY=[]
        eggY_change = []

        rows = 2 + level
        if rows > 5:
            rows = 5
        num_of_enemies = 8*rows
        ygap = 0
        for j in range(rows):
            for i in range(8):
                enemyimg.append(pygame.image.load("redchicken.png"))
                enemyX.append(i*200)
                enemyY.append(ygap)
                enemyX_change.append(5)
                enemyY_change.append(40)
                eggimg.append(pygame.image.load("001-egg.png"))
                egg_state.append("ready")
                eggX.append(0)
                eggY.append(0)
                eggY_change.append(5)
            ygap += 100

        #display enemy
        def enemy(x,y,i):
            screen.blit(enemyimg[i],(x,y))

        missileimg = []
        missileX=[]
        missileY=[]
        missileX_change = []
        missileY_change=[]
        missile_state = []
        for i in range(10):
            missileimg.append(pygame.image.load("001-computer.png"))
            missileX.append(0)
            missileY.append(480)
            missileX_change.append(0)
            missileY_change.append(5)
            missile_state.append("ready")

        def fire_missile(x,y,i):
            global missile_state
            missile_state[i] = "fire"
            screen.blit(missileimg[i],(x+16,y+64))

        dct = {"pygame.K_0": pygame.K_0,"pygame.K_1": pygame.K_1,"pygame.K_2": pygame.K_2,"pygame.K_3": pygame.K_3,"pygame.K_4": pygame.K_4,"pygame.K_5": pygame.K_5,"pygame.K_6": pygame.K_6,"pygame.K_7": pygame.K_7,"pygame.K_8": pygame.K_8,"pygame.K_9": pygame.K_9} 


        def iscollision(enemyX,enemyY,missileX,missileY):
            distance = math.sqrt((math.pow((enemyX-missileX),2))+(math.pow((enemyY-missileY),2)))
            if distance < 60:
                return True
            return False

        def drop_egg(x,y,i):
            global eggstate
            egg_state[i] = "drop"
            screen.blit(eggimg[i],(x-16,y+10))



        counts = 50
        lives = 3
        enemies = num_of_enemies
        running = True
        while running:
            text = base_font.render(f"Lives: {lives}",True,(255,255,255))
            screen.fill((0,0,0))
            screen.blit(background,(0,0))
            #quiting the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    runningmain = False
                #movement of the spaceship
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        changex = 6 
                    if event.key == pygame.K_LEFT:
                        changex = -6
                    for i in range(10):
                        if event.key == dct[f"pygame.K_{i}"]:
                            if missile_state[i] == "ready":
                                missileX[i] = shipx
                                fire_missile(missileX[i],missileY[i],i)  
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        changex = 0
            if shipx <= 0:
                shipx = 0
            elif shipx >= 1470:
                shipx = 1470
            #blitting and movement of enemies
            for i in range(num_of_enemies):
                enemyX[i] += enemyX_change[i]
                if enemyX[i]<= 0:
                    enemyX_change[i] = 5 + level
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 1400:
                    enemyX_change[i] = -5 - level
                    enemyY[i] += enemyY_change[i]
                enemy(enemyX[i],enemyY[i],i)
            for i in range(10):
                if missileY[i]<= 0:
                    missileY[i] = 480
                    missile_state[i] = "ready"
                
                if missile_state[i] == "fire":
                    fire_missile(missileX[i],missileY[i],i)
                    missileY[i] -= missileY_change[i]
            for j in range(10):
                for i in range(num_of_enemies):
                    collision = iscollision(enemyX[i],enemyY[i],missileX[j],missileY[j])
                    if collision:
                        explosion_sound = mixer.Sound("explosion.wav")
                        explosion_sound.play()
                        missileY[j] = 480
                        missile_state[j] = "ready"
                        enemyX[i] = 0
                        enemyY[i] = -10000
                        enemies -= 1
            for i in range(num_of_enemies):
                collision2 = iscollision(shipx,shipy,eggX[i],eggY[i])
                if collision2:
                    egg_sound = mixer.Sound("egg crack.mp3")
                    egg_sound.play()
                    eggX[i] = 5000
                    lives -= 1

            if lives == 0:
                display = 3
                running = False


            
            if counts < 0:
                i = random.randint(0,num_of_enemies-1)
                eggX[i]= enemyX[i]
                eggY[i] = enemyY[i] + 65
                drop_egg(eggX[i],eggY[i],i)
                counts = 50
            for i in range(num_of_enemies):
                if eggY[i] > 802:
                    eggY[i] = -800
                    egg_state[i] = "ready"
                
                if egg_state[i] == "drop":
                    drop_egg(eggX[i],eggY[i],i)
                    eggY[i] += eggY_change[i]

            for i in range(num_of_enemies):
                if enemyY[i] > 700:
                    display = 3
                    running = False
                    break
            if enemies == 0:
                display = 1
                running = False
                
            counts -= 1 + (2*level)
            shipx += changex
            screen.blit(spaceship,(shipx,shipy))
            screen.blit(text,(10,10))
            pygame.display.update()
    if display == 1:
        level += 1
        level_up_sound = mixer.Sound("level increase.wav")
        level_up_sound.play()
        background = pygame.image.load("bg.png")
        base_font = pygame.font.Font("freesansbold.ttf",72)
        text = base_font.render(f"Level {level+1}",True,(255,255,255))
        walking = True
        while walking:
            screen.fill((0,0,0))
            screen.blit(background,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    walking = False
                    runningmain = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    display = 2
                    walking = False
            screen.blit(text,(660,370))
            pygame.display.update()
    if display == 3:
        mixer.music.stop()
        base_font = pygame.font.Font("freesansbold.ttf",72)
        text = base_font.render(f"GAME OVER",True,(255,255,255))
        game_over_sound = mixer.Sound("game over.wav")
        game_over_sound.play()
        walking = True
        while walking:
            screen.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    walking = False
                    runningmain = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    display = 0
                    walking = False
            screen.blit(text,(550,370))
            pygame.display.update()
                    
pygame.quit()
