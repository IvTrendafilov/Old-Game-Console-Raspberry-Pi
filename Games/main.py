import pygame
import pygame_menu
from pygame_menu.themes import Theme
from games import pong

import time

pygame.init()
# This function takes the max size of a display
infoObject = pygame.display.Info()
# We make the display to be full screen
surface = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
mainMenuBackground = pygame_menu.baseimage.BaseImage("background-mainmenu.jpg", pygame_menu.baseimage.IMAGE_MODE_FILL,
                                                     (0, 0))

retroTheme = Theme()

# Background picture
retroTheme.background_color = mainMenuBackground

# Fonts
retroTheme.title_font = pygame_menu.font.FONT_8BIT
retroTheme.widget_font = pygame_menu.font.FONT_8BIT

# Setup GPIO
# UNCOMMENT WHEN YOU TRY IT WITH SENSORS
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(7.GPIO.IN) #ARROW UP
# GPIO.setup(8.GPIO.IN) #ARROW DOWN
# GPIO.setup(11.GPIO.IN) #ARROW LEFT
# GPIO.setup(12.GPIO.IN) #ARROW RIGHT

score = 0
def pongGame():
    gameMenu.disable()
    global score
    score = pong.startGame()
    scoreEndGame.set_title("Score: " + str(score))
    endGameMenu.enable()
    pass


def shmupGame():

    pass


def game3():
    pass


def enterChooseGameMenu():
    gameMenu.enable()
    mainMenu.disable()


def exitChooseGameMenu():
    gameMenu.disable()
    mainMenu.enable()


def enterSettingsMenu():
    settingsMenu.enable()
    mainMenu.disable()


def exitSettingsMenu():
    settingsMenu.disable()
    mainMenu.enable()


def exitEndGameMenu():
    endGameMenu.disable()
    mainMenu.enable()


# Main Menu configuration
mainMenu = pygame_menu.Menu(infoObject.current_h, infoObject.current_w, title='Welcome to retro game arcade',
                            theme=retroTheme, mouse_enabled=False)
mainMenu.add_button('Choose a game', enterChooseGameMenu)
mainMenu.add_button('Settings', enterSettingsMenu)
mainMenu.add_button('Quit', pygame_menu.events.EXIT)

# Choose a game menu configuration
gameMenu = pygame_menu.Menu(infoObject.current_h, infoObject.current_w, title='Welcome to retro game arcade',
                            theme=retroTheme, mouse_enabled=False)
gameMenu.add_button('Pong', pongGame)
gameMenu.add_button('Shooters', shmupGame)
gameMenu.add_button('Game 3', game3)
gameMenu.add_button('Back', exitChooseGameMenu)
gameMenu.disable()

# Settings menu configuration
settingsMenu = pygame_menu.Menu(infoObject.current_h, infoObject.current_w, title='Settings',
                                theme=retroTheme, mouse_enabled=False)
settingsMenu.add_text_input('Name :', default='Enter you name')
settingsMenu.add_selector('Test :', [('test1', 1), ('test2', 2)])
settingsMenu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)])
settingsMenu.add_button('Save', pongGame)
settingsMenu.add_button('Back', exitSettingsMenu)
settingsMenu.disable()

# End of game menu
endGameMenu = pygame_menu.Menu(infoObject.current_h, infoObject.current_w, title='Game Over',
                               theme=retroTheme, mouse_enabled=False)
scoreEndGame = endGameMenu.add_label("Score: " + str(score), selectable=False)
tryAgainButton = endGameMenu.add_button('Try again', pongGame)
endGameMenu.add_button('Go to main menu', exitEndGameMenu)
endGameMenu.disable()

while True:
    # if GPIO.input(7): #ARROW UP
        # mainMenu._select(mainMenu.get_index() - 1, 2)
        # time.sleep(0.2)
    # if GPIO.input(8): #ARROW DOWN
        # mainMenu._select(mainMenu.get_index() + 1, 0)
        # time.sleep(0.2)
    # if GPIO.input(12): #ARROW RIGHT
        # mainMenu.get_selected_widget().apply()
        # time.sleep(0.2)
    #WE DO NOT NEED ARROW LEFT FOR NOW
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
    if settingsMenu.is_enabled() and inMainMenu == False:
        settingsMenu.update(events)
        if settingsMenu.is_enabled():
            settingsMenu.draw(surface)
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
