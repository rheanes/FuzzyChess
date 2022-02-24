# FuzzyChess
Senior Project Chess AI Variant 

main.py tracks the current gamestate and executes functions and switched to scenes depending on the current gamestate

Images Folder contains all of the images that we are using in our project.

--------------SCENES--------------------------------
GameScene.py -
Has the creation for our game. It draws the board and puts the pieces on our board. 
It also tracks the logic of the game. 

RulesScene.py - This is the scene that draws the rules page to the screen. 

HowToPlay.py - This is the scene that describes the different actions a user can perform. 

PiecesScene.py - This is the scene that will give general information about the pieces. Including the capture table.

PawnScene.py - This is the scene that will display all the information about the pawns to the screen.

KnightScene.py - This is the scene that will display all the information about the knights to the screen.

RookScene.py - This is the scene that will display all the information about the rooks to the screen.

QueenScene.py - This is the scene that will display all the information about the queens to the screen.

BishopScene.py - This is the scene that will display all the information about the bishops to the screen. 

KingScene.py - This is the scene that will display all the information about the kings to the screen. 

MainMenuScene.py - This is the scene that will draw or main menu to the screen.

-----------------------------------------------------------

RulesPageCommon.py - Contains all of the elements that are common between the different scenes within the rules page and puts them on the scene.
Common.py contains common elements that are used in multiple different files. It has screen size and colors and fonts all defined here.

ai.py - contains everything to do with out ai here.

board.py - 
contains all of the board information we need. It defines squares and has the create board function. 
It also has board utility here like piece movment and square coordinate finding. 
Any square highlighting and unhighlighting and pathfinding for our pieces is found here.

pieces.py - 
contains everything to do with our pieces. Our ccommanders are also created in this file. The movment for pawns is also defined here. 

GameFunctions.py -
contains basic game functions here. This includes deligation, turn managment, dice rolling, and attacking. 

guielements.py - contains all of our custom made GUIElements, including buttons. 

