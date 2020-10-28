import pygame, sys, random
from pygame import key
import RPi.GPIO as GPIO
import time



def startGame():
    pygame.init()
    width = 1500
    height = 1000
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")

    ball = pygame.image.load("images/beach-ball.png")
    ballrect = ball.get_rect()
    ballrect.top = random.randint(0, 800)
    ballrect.left = 150

    line = pygame.image.load("images/line.png")
    linerect = line.get_rect()
    linerect.top = height / 2
    linerect.left = 40

    score = 0
    largeFont = pygame.font.SysFont('comicsans', 50)  # Font object

    inGame = True
    speed = [2,2]
    black = 0, 0, 0

    while inGame:

        GPIO.setup(15, GPIO.IN)  # ARROW UP
        # GPIO.setup(8.GPIO.IN) #ARROW DOWN
        #     GPIO.setup(13.GPIO.IN) #ARROW LEFT
        GPIO.setup(13, GPIO.IN)  # ARROW RIGHT
        if GPIO.input(15):  # ARROW UP
             if linerect.top > 0:
                  linerect.top = linerect.top - 3
                  time.sleep(0.3)
        # if GPIO.input(8): #ARROW DOWN
        # mainMenu._select(mainMenu.get_index() + 1, 0)
        # time.sleep(0.2)
        if GPIO.input(13):  # ARROW RIGHT or ARROW DOWN for Pong game
            if linerect.top < height - 93:
                  linerect.top = linerect.top + 3
                  time.sleep(0.3)
        # WE DO NOT NEED ARROW LEFT FOR NOW
        GPIO.setup(13, GPIO.OUT)
        GPIO.output(13, GPIO.LOW)
        GPIO.setup(15, GPIO.OUT)
        GPIO.output(15, GPIO.LOW)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Line controller
        #key = pygame.key.get_pressed()
        #if key[pygame.K_DOWN]:
            #if linerect.top < height - 93:
                #linerect.top = linerect.top + 3
        #if key[pygame.K_UP]:
            #if linerect.top > 0:
                #linerect.top = linerect.top - 3

        # Ball movement
        ballrect = ballrect.move(speed)
        if ballrect.left < 130 or ballrect.right > width:
            if ballrect.left < 130:
                pygame.display.set_caption("Main Menu!")
                return score
            else:
                speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]
        if ballrect.colliderect(linerect):
            speed[0] = -speed[0]
            score = score + 1

        text = largeFont.render('Score: ' + str(score), 1, (255, 255, 255))
        screen.fill(black)
        screen.blit(ball, ballrect)
        screen.blit(line, linerect)
        screen.blit(text, (10, 10))
        pygame.display.flip()


