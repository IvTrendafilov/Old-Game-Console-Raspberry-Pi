import pygame, sys, random
from pygame import key



def startGame():
    pygame.init()
    width = 1500
    height = 1000
    screen = pygame.display.set_mode((width, height))

    ball = pygame.image.load("beach-ball.png")
    ballrect = ball.get_rect()
    ballrect.top = random.randint(0, 1000)
    ballrect.left = 100

    line = pygame.image.load("line.png")
    linerect = line.get_rect()
    linerect.top = height / 2
    linerect.left = 40

    score = 0
    largeFont = pygame.font.SysFont('comicsans', 50)  # Font object

    inGame = True
    speed = [2,2]
    black = 0, 0, 0

    while inGame:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        # Line controller
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            if linerect.top < height - 93:
                linerect.top = linerect.top + 3
        if key[pygame.K_UP]:
            if linerect.top > 0:
                linerect.top = linerect.top - 3

        # Ball movement
        ballrect = ballrect.move(speed)
        if ballrect.left < 39 or ballrect.right > width:
            if ballrect.left < 39:
                return score
            else:
                speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]
        if ballrect.colliderect(linerect):
            speed[1] = -speed[1]
            speed[0] = -speed[0]
            score = score + 1

        text = largeFont.render('Score: ' + str(score), 1, (255, 255, 255))
        screen.fill(black)
        screen.blit(ball, ballrect)
        screen.blit(line, linerect)
        screen.blit(text, (10, 10))
        pygame.display.flip()


