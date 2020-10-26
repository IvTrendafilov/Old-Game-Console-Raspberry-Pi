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
mainmenuBackground = pygame_menu.baseimage.BaseImage("background-mainmenu.jpg", pygame_menu.baseimage.IMAGE_MODE_FILL,
                                                     (0, 0))

retroTheme = Theme()

# Background picture
retroTheme.background_color = mainmenuBackground

# Fonts
retroTheme.title_font = pygame_menu.font.FONT_8BIT
retroTheme.widget_font = pygame_menu.font.FONT_8BIT

# Setup GPIO


score = 0

def game1():
    gameMenu.disable()
    score = pong.startGame() #FIX AS IT DOES NOT CHANGE THE SCORE VARIABLE
    endGameMenu.enable()
    pass


def game2():
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
gameMenu.add_button('Game 1', game1)
gameMenu.add_button('Game 2', game2)
gameMenu.add_button('Game 3', game3)
gameMenu.add_button('Back', exitChooseGameMenu)
gameMenu.disable()

# Settings menu configuration
settingsMenu = pygame_menu.Menu(infoObject.current_h, infoObject.current_w, title='Settings',
                                theme=retroTheme, mouse_enabled=False)
settingsMenu.add_text_input('Name :', default='Enter you name')
settingsMenu.add_selector('Test :', [('test1', 1), ('test2', 2)])
settingsMenu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)])
settingsMenu.add_button('Save', game1)
settingsMenu.add_button('Back', exitSettingsMenu)
settingsMenu.disable()

#End of game menu
endGameMenu = pygame_menu.Menu(infoObject.current_h, infoObject.current_w, title='Game Over',
                 theme=retroTheme, mouse_enabled=False)
endGameMenu.add_label("Score: " + str(score),selectable=False)
endGameMenu.add_button('Try again', game1)
endGameMenu.add_button('Go to main menu', exitEndGameMenu)
endGameMenu.disable()

firstTime = True
while True:

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            exit()

    inMainMenu=False
    inGameMenu=False
    if mainMenu.is_enabled():
        inMainMenu=True
        mainMenu.update(events)
        if mainMenu.is_enabled():
            mainMenu.draw(surface)
    if settingsMenu.is_enabled() and inMainMenu == False:
        settingsMenu.update(events)
        if settingsMenu.is_enabled():
            settingsMenu.draw(surface)
    if gameMenu.is_enabled() and inMainMenu == False:
        inGameMenu=True
        gameMenu.update(events)
        if gameMenu.is_enabled():
            gameMenu.draw(surface)
    if endGameMenu.is_enabled() and inGameMenu == False and inMainMenu==False:
        endGameMenu.update(events)
        if endGameMenu.is_enabled():
            endGameMenu.draw(surface)

    pygame.display.update()


