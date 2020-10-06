#SOFTWARE DESIGN DOCUMENT

|                 | **Names/Ids**  |
|----------------:|:---------------|
| *Team members:* |Stefan Ilich, Ivan Trendafilov, Vladi Avramov, Pavel Hristov, Tudor Nechiti, Stefan Simionescu                |
| *Team ID:*      |        28        |
 

## Introduction

The Interactive Game Console (IC) at a basic level aims to deliver the same experience other consoles do - effortless enjoyment of time spent. The advantage of a console for gaming has always been the simplicity of action – you just plug and play, and that’s what always differentiated it from the PC, it is simple to use and also brings some features not present on the PC. In that sense, our system aims to deliver the simple and reliable experience, but also introduce an important feature – new controls. The way a user interacts with a game is always through the controller, but traditional controllers have been around for more than a decade now and we wanted to rework a little bit the feel of controlling the game so we decided to go with a new touch control sensor system. After going through some ideas we decided to pair two different ideas that might work great together – old school games and new controlling schemes. In that way we can revitalize a small part of the old school genre through the means of modern input and experience, while retaining the old school look and gameplay. For this type of undertaking we needed the proper hardware – Raspberry Pi 4, some touch sensors, for a basic version of the product. We also have to pair it up with a pleasing and easy to understand user interface, which at the same time has to always stay responsive to the player input. Combining those ideas will result in a very nice way to revisit some old classics that we always wanted to and bring that arcade feel to other people as well. We will present our ideas through the means of some UML diagrams, mockup, requirements and fail states we derived, milestones that we have to achieve in development, how we prioritize the requirements and finally a conclusion to the whole design.

## Product User Interface

Diagram 1
The picture is our activity diagram. Firstly, the player must turn on the console to have access to all the options we offer. After powering up, the system will display its user-friendly interface, where the player can choose from 3 options - to edit settings, to pick a game or to exit. When a game is picked, the system will automatically start it. While in-game, every player has the option to restart or exit the game. If one exits or finishes the game, he will be forwarded to the main menu once more.

Diagram 2
The picture is our sequence diagram. After powering on, when clicking, the player will execute the pickAnOption function, which will forward him to the next step, which will be to pick a game, change settings or exit. If a game is picked, startGame() function will start. Afterwards a loop, which includes input from the touch sensors, will trigger the makeMove() function. If the player decides to change settings, this will happen as follows. After clicking the save button the state of his changed settings will be sent with the changeSettings() function, which will result in putting the new state in the place of the old one.

Diagram 3
The picture is our Use case diagram. We have chosen the player to be the only actor in this diagram because  he controls the system and does all the actions by using the console. He can turn the console on and off and of course restart it. By console we essentially mean here the user interface which is used to do all the other actions. While in the console a player can start a game, change the settings or see all the highscores for the different games. Furthermore we have a use case for playing a game. This use case has a few extension points. These points are use cases that might happen or might not. Examples are:
Pausing a game: A player may decide to pause a game
Exiting a game: A player may decide to quit halfway through
Using touch sensor and using motion sensor. These are extension points because a player may use on or the other depending on the game. 
Last but not least we have finishing a game. This is an extend because a game might not be finished.

MockUp

## Requirements/System Overview 

As a player, I want to navigate through the interface using the touch sensors provided.

As a player, I want to be presented with a user-friendly interface.

As a player, I want to be able to select from a variety of available games that suit my liking.

As a player, I want to be able to pause/resume/restart/exit a game by making use of the intuitive application’s interface.

As a player, I want to be able to be presented with a variety of instructions, such as: game controls or game rules that will improve my overall 
gaming experience.

As a player, I want to be able to change the settings such as game difficulty / display size within Interactive Game Console in a way that complies with my preferences.

As a player, I want to be presented with a score and progress on each game that I play.

The system itself recognizes touch/motion sensors and provides responsiveness.

The system will support different types of users ranging from children to teenagers or adults and the difficulty of the games will vary, depending on 
the skill level of a specific user. A shor user manual and instructions will be provided in the game menu, in order to allow users to fully understand and utilize the system.

The system will use a moderate font size that prevents eye strain. Furthermore, vibrant screen flashes will be kept to a minimum to accommodate those prone to epileptic seizures.

In the unusual case of a system failure, the system itself issues a backup of all the game data and terminates all the ongoing processes. It then tries to recover its previous state by restarting the application. 


## Milestones

We decided that the first milestone will be connecting the touch sensors to the Raspberry more in depth giving and receiving input. We decided to place this as the first milestone because for the display interface and games to work we need to somehow implement commands.

The second milestone will be the display interface. We think that this is the second most important milestone as we need an interface for the user. In this milestone we want to have an interface in which the user can operate freely without any confusion. This interface will also be the intertwining point between the different games.

The third milestone will be creating and connecting the first game with the touch sensors and the display interface. This is the third milestone because here we will see if the display interface works well with the game and we will also see if the touch sensors work correctly with the game that we created.

The fourth milestone is creating and connecting multiple games. We decided this to be the fourth milestone as we will now have multiple games from which the user can choose in the display interface and see if everything goes by smoothly without any problems.

The fifth and last milestone will be additional options for games. Such as the highest score, scoreboard of different users and so on.


## Requirement Priorities

Have responsive sensors(touch): The first and most important functionality is the touch sensors. We need to make sure that every touch sensor performs the action which it should without any problems or delays.

Have a working display interface: The second most important functionality is having a display interface. If we don’t count the sensors this is the most important functionality from a user standpoint. We need the interface because this is where all the games will be interconnected. From this interface the user can choose from different games which he could play. He can also choose if he wants to pause the game, resume the game or quit the game. He can also choose if he wants to exit the user interface.

Have working game/s: The third functionality is having 1 game. We need to have 1 game in order to test if everything works well with the sensors and the display interface

Have options to choose between games: The fourth minimal product is having at least 2 working games. We need to have at least 2 games which will be connected to the display interface and from which the player can choose.

## Conclusion

In conclusion, we would like to say that we undoubtedly know that it won’t be easy to follow through on all our milestones. We know creating multiple games with sensor controls will be a challenge but nevertheless want to give it our best and create an amazing Retro Gaming Console. We do not want people to forget the classics because they mark the beginning of the gaming industry. We want to give them this gaming experience through modern means of interaction because we know that nowadays there are not so many arcades that contain classic games. By showing our users some classic games we hope to encourage them to create more and add them to our console in order to revive some of the older games and maybe give them more modern designs. We know that the current generation doesn't know and care about the games of the previous generation so what we want to achieve with this project is to demonstrate that older games can also be fun. Last but not least we are of course doing this for ourselves. We want to improve our understanding of Raspberry Pi and our teamwork and programming skills. That is why as you can see our design is minimalistic. We will simply create a user interface and a few games. We have prioritized the creation of at least one game but hope to have two games ready by the end of the project. Things like highscores and changing difficulty are our last concern because we want to focus on delivering a good gaming experience without bugs on top of everything else.

## Reference
