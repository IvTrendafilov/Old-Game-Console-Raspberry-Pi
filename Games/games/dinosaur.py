# pictures taken from https://drive.google.com/drive/folders/1-gJcrlg64ECgMii-rDCu8MJYXN4IUr4k
# tutorial watched for the completion of the game https://www.youtube.com/watch?v=FfWpgLFMI7w&t=6997s

import pygame
import math
import random
import RPi.GPIO as GPIO


# https://www.youtube.com/watch?v=CY4aMq3t3QE&list=PLnqEPPFiEkRfapYiYlfD2pyIYGLyVY2WL&index=7


pygame.init()

screen = pygame.display.set_mode((600, 500))

pygame.display.set_caption("Internetless T-Rex")
littleIcon = pygame.image.load('./games/dinoimages/1.png')
pygame.display.set_icon(littleIcon)

treeImage0 = pygame.image.load('./games/dinoimages/tree.PNG')
treeImage0 = pygame.transform.scale(treeImage0, (90, 50))
treeImage1 = pygame.image.load('./games/dinoimages/tree1.PNG')
treeImage1 = pygame.transform.scale(treeImage1, (80, 70))
treeImage2 = pygame.image.load('./games/dinoimages/tree2.PNG')
treeImage2 = pygame.transform.scale(treeImage2, (80, 65))
treeImage3 = pygame.image.load('./games/dinoimages/tree3.PNG')
treeImage3 = pygame.transform.scale(treeImage3, (80, 40))
treeImage4 = pygame.image.load('./games/dinoimages/tree4.PNG')
treeImage4 = pygame.transform.scale(treeImage4, (90, 60))
treeImage5 = pygame.image.load('./games/dinoimages/tree5.PNG')
treeImage5 = pygame.transform.scale(treeImage5, (70, 50))

backgroundImage = pygame.image.load('./games/dinoimages/background.png')


plImage = pygame.image.load('./games/dinoimages/dino.png')
plImage = pygame.transform.scale(plImage, (45, 45))
plImage1 = pygame.image.load('./games/dinoimages/dra3.png')
plImage1 = pygame.transform.scale(plImage1, (50, 50))
plImage2 = pygame.image.load('./games/dinoimages/dra4.png')
plImage2 = pygame.transform.scale(plImage2, (50, 50))


run = [plImage1, plImage1, plImage1, plImage2, plImage2, plImage2, plImage1, plImage1, plImage1, plImage2, plImage2,
       plImage2, plImage1, plImage1, plImage1, plImage2, plImage2, plImage2]


font = pygame.font.Font('freesansbold.ttf', 32)
score_val = 0

scoreX = 10
scoreY = 10

over_font = pygame.font.Font('freesansbold.ttf', 20)

overX = 150
overY = 150


# def game_Over(v, b):
#     game_over = over_font.render("Game over. Your score was " + str(score_val), True, (0, 0, 0))
#     screen.blit(game_over, (v, b))
#
#e това би трябвало да ти трябва за скора ама не знам защо не работи
# def showScore(x, y):
#     score = font.render("Score :" + str(score_val), True, (0, 0, 0))
#     screen.blit(score, (x, y))


def backgroundd(q, w):
    screen.blit(backgroundImage, (q, w))


# def player(e,r):
#     screen.blit(plImage,(e, r))


def tree0(t, y):
    screen.blit(treeImage0, (t, y))


def tree1(t, y):
    screen.blit(treeImage1, (t, y))


def tree2(t, y):
    screen.blit(treeImage2, (t, y))


def tree3(t, y):
    screen.blit(treeImage2, (t, y))


def tree4(t, y):
    screen.blit(treeImage4, (t, y))


def tree5(t, y):
    screen.blit(treeImage5, (t, y))


# def Col(plX, plY, tree0X, tree0Y):
#     distance = math.sqrt((math.pow(plX - tree0X, 2)) + (math.pow(plY - tree0Y, 2)))
#     if distance < 27:
#         return True


goUp = 3
goDown = 3

#май това е метода дето искаш
def gameloop():
    score_val = 0
    runp = 0
    gameOver = False
    jump = False
    plX = 50
    plY = 275
    tree0X = 450
    tree0Y = 285
    backX = 0
    backY = 0
    backMovement = 0.0
    running = True
    while running:
        backMovement = -2
        screen.fill((255, 255, 255))
        GPIO.setup(40, GPIO.OUT)
        GPIO.output(40, GPIO.LOW)
        GPIO.setup(40, GPIO.IN)  #ARROW UP
        if GPIO.input(40):
            if 275 >= plY >= 250:
                jump = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # print(backMovement)
        backX += backMovement
        # print(backX)
        tree0X += backMovement
        # print(tree0X)
        backgroundd(backX, backY)

        backgroundd(backX + 600, backY)

        tree0(tree0X, tree0Y)

        tree1(tree0X + 400, tree0Y - 10)

        tree2(tree0X + 950, tree0Y - 5)

        tree3(tree0X + 1350, tree0Y - 4)

        tree4(tree0X + 1700, tree0Y - 4)

        tree5(tree0X + 2000, tree0Y - 4)

        if backX == -600:
            backX = 0

        if tree0X < -2100:
            tree0X = 550

        if 276 > plY > 125:

            if jump == True:
                plY -= goUp
        else:

            jump = False

        if plY <= 274:

            if jump == False:
                plY += goDown

        if tree0X < plX + 40 < tree0X + 80 and tree0Y < plY + 50 < tree0Y + 50:
            backMovement = 0.0
            runp = 0
            gameOver = True

        if tree0X + 400 < plX + 40 < tree0X + 470 and tree0Y < plY + 50 < tree0Y + 50:
            backMovement = 0.0
            runp = 0
            gameOver = True

        if tree0X + 950 < plX + 40 < tree0X + 1050 and tree0Y < plY + 50 < tree0Y + 50:
            backMovement = 0.0
            runp = 0
            gameOver = True

        if tree0X + 1350 < plX + 40 < tree0X + 1450 and tree0Y < plY + 50 < tree0Y + 50:
            backMovement = 0.0
            runp = 0
            gameOver = True

        if tree0X + 1700 < plX + 40 < tree0X + 1770 and tree0Y < plY + 50 < tree0Y + 50:
            backMovement = 0.0
            runp = 0
            gameOver = True

        if tree0X + 2000 < plX + 40 < tree0X + 2070 and tree0Y < plY + 50 < tree0Y + 50:
            backMovement = 0.0
            runp = 0
            gameOver = True

        # collision = Col(plX,plY,tree0X,tree0Y)
        # if collision:
        #     backMovement = 0
        #     runp = 0
        if gameOver == True:
            game_over = over_font.render("Game over. Pres down arrow to replay " , True, (0, 0, 0))
            screen.blit(game_over, (100, 150))
            return round(score_val)
        else:
            score_val += 0.01
        screen.blit(run[runp], (plX, plY))
        runp += 1
        if runp > 8:
            runp = 0
        score = font.render("Score :" + str(round(score_val)), True, (0, 0, 0))
        screen.blit(score, (10, 10))
        pygame.display.update()
