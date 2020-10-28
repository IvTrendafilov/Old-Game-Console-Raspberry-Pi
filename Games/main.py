import pygame
import pygame_menu
from pygame_menu.themes import Theme
from games import pong,shmup
import RPi.GPIO as GPIO

import time

pygame.init()
# This function takes the max size of a display
infoObject = pygame.display.Info()
# We make the display to be full screen
surface = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
mainMenuBackground = pygame_menu.baseimage.BaseImage("images/background-mainmenu.jpg", pygame_menu.baseimage.IMAGE_MODE_FILL,
                                                     (0, 0))

retroTheme = Theme()

# Background picture
retroTheme.background_color = mainMenuBackground

# Fonts
retroTheme.title_font = pygame_menu.font.FONT_8BIT
retroTheme.widget_font = pygame_menu.font.FONT_8BIT

# Setup GPIO
# UNCOMMENT WHEN YOU TRY IT WITH SENSORS
GPIO.setmode(GPIO.BOARD)


score = 0
def pongGame():

    gameMenu.disable()
    global score
    score = pong.startGame()
    global surface
    surface = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
    scoreEndGame.set_title("Score: " + str(score))
    tryAgainButton.update_callback(pongGame)
    highScores = open("pongHighScores.txt","a")
    highScores.write(str(score)+"\n")
    endGameMenu.enable()
    pass


def shmupGame():
    gameMenu.disable()
    global score
    score = shmup.main()
    global surface
    surface = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
    scoreEndGame.set_title("Score: " + str(score))
    tryAgainButton.update_callback(shmupGame)
    highScores = open("shootersHighScores.txt", "a")
    highScores.write(str(score) + "\n")
    endGameMenu.enable()
    pass


def flappyBird():
    pass

def enterHighScorePong():
    file = open("pongHighScores.txt", "r")
    d = file.readlines()
    d.sort(reverse=True)

def exitHighScorePong():
    pass

def enterHighScoreShooters():
    pass

def exitHighScoreShooters():
    pass

def enterHighScoreFlappyBird():
    pass

def exitHighScoreFlappyBird():
    pass

def enterChooseGameMenu():
    gameMenu.enable()
    global currentMenu
    currentMenu=gameMenu
    mainMenu.disable()


def exitChooseGameMenu():
    gameMenu.disable()
    global currentMenu
    currentMenu=mainMenu
    mainMenu.enable()


def enterHighScoreMenu():
    highScoreMenu.enable()
    global currentMenu
    currentMenu=highScoreMenu
    mainMenu.disable()


def exitHighScoreMenu():
    highScoreMenu.disable()
    global currentMenu
    currentMenu=mainMenu
    mainMenu.enable()


def exitEndGameMenu():
    endGameMenu.disable()
    global currentMenu
    currentMenu=mainMenu
    mainMenu.enable()

pygame.display.set_caption("Main Menu!")
pygame.display.set_icon(pygame.image.load("images/retroIcon.png"))

# Main Menu configuration
mainMenu = pygame_menu.Menu(infoObject.current_h, infoObject.current_w, title='Welcome to retro game arcade',
                            theme=retroTheme, mouse_enabled=False)
mainMenu.add_button('Choose a game', enterChooseGameMenu)
mainMenu.add_button('High scores', enterHighScoreMenu)
mainMenu.add_button('Quit', pygame_menu.events.EXIT)

# Choose a game menu configuration
gameMenu = pygame_menu.Menu(infoObject.current_h, infoObject.current_w, title='Welcome to retro game arcade',
                            theme=retroTheme, mouse_enabled=False)
gameMenu.add_button('Pong', pongGame)
gameMenu.add_button('Shooters', shmupGame)
gameMenu.add_button('Game 3', flappyBird)
gameMenu.add_button('Back', exitChooseGameMenu)
gameMenu.disable()

# Settings menu configuration
highScoreMenu = pygame_menu.Menu(infoObject.current_h, infoObject.current_w, title='Settings',
                                 theme=retroTheme, mouse_enabled=False)
highScoreMenu.add_button("Pong",enterHighScorePong)
highScoreMenu.add_button("Shooters",enterHighScoreShooters)
highScoreMenu.add_button("Flappy Bird",enterHighScoreFlappyBird)
highScoreMenu.add_button('Back', exitHighScoreMenu)
highScoreMenu.disable()

# End of game menu
endGameMenu = pygame_menu.Menu(infoObject.current_h, infoObject.current_w, title='Game Over',
                               theme=retroTheme, mouse_enabled=False)
scoreEndGame = endGameMenu.add_label("Score: " + str(score), selectable=False)
tryAgainButton = endGameMenu.add_button('Try again', pongGame)
endGameMenu.add_button('Go to main menu', exitEndGameMenu)
endGameMenu.disable()

#High score display
highScoreDisplay = pygame_menu.Menu(infoObject.current_h, infoObject.current_w, title='High Scores',
                                 theme=retroTheme, mouse_enabled=False)
highScoreDisplay.disable()
currentMenu=mainMenu
while True:
    GPIO.setup(15,GPIO.IN) #ARROW UP
    # GPIO.setup(8.GPIO.IN) #ARROW DOWN
#     GPIO.setup(13.GPIO.IN) #ARROW LEFT
    GPIO.setup(13,GPIO.IN) #ARROW RIGHT
    if GPIO.input(15): #ARROW UP
        currentMenu._select(currentMenu.get_index() + 1, 2)
        time.sleep(0.3)
    # if GPIO.input(8): #ARROW DOWN
        # mainMenu._select(mainMenu.get_index() + 1, 0)
        # time.sleep(0.2)
    if GPIO.input(13): #ARROW RIGHT
        currentMenu.get_selected_widget().apply()
        time.sleep(0.3)
    #WE DO NOT NEED ARROW LEFT FOR NOW
    GPIO.setup(13,GPIO.OUT)
    GPIO.output(13,GPIO.LOW)
    GPIO.setup(15,GPIO.OUT)
    GPIO.output(15,GPIO.LOW)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            exit()

    inMainMenu = False
    inGameMenu = False
    if mainMenu.is_enabled():
        inMainMenu = True
        mainMenu.update(events)
        if mainMenu.is_enabled():
            mainMenu.draw(surface)
    if highScoreMenu.is_enabled() and inMainMenu == False:
        highScoreMenu.update(events)
        if highScoreMenu.is_enabled():
            highScoreMenu.draw(surface)
    if gameMenu.is_enabled() and inMainMenu == False:
        inGameMenu = True
        gameMenu.update(events)
        if gameMenu.is_enabled():
            gameMenu.draw(surface)
    if endGameMenu.is_enabled() and inGameMenu == False and inMainMenu == False:
        endGameMenu.update(events)
        if endGameMenu.is_enabled():
            endGameMenu.draw(surface)

    pygame.display.update()
