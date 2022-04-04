from guielements import *

from GameScene import playgame, delegation_mode, turnChange, create_board, reset_turn, update_display
from board import *
from Scenes.MainMenuScene import MenuScene
from Scenes.RulesPageScene import RulesPageScene
from Scenes.HowToPlay import HowToPlayScene
from Scenes.PiecesScene import PiecesScene
from Scenes.PawnScene import PawnScene
from Scenes.RookScene import RookScene
from Scenes.KnightScene import KnightScene
from Scenes.QueenScene import QueenScene
from Scenes.BishopScene import BishopScene
from Scenes.KingScene import KingScene
from Scenes.winLossScreen import winLossScreen
from Scenes.EscapeScene import escapeScene
from Scenes.NewOrLoadScene import NewOrLoadScene
from AiScene import aigame
from board import remove_highlights

#pygame.mixer.music.load("Ciara's First Beat.mp3")
#pygame.mixer.music.play(-1)

#TODO add some functionality for continue game. This entails adding a game exists button
#I need to make buttons not appear if they cant be called.
#So if there is no current game, then save should not be an option. If there is no current game then continue should
#not be an option
#for the rules page make the button in the top right take you back to where it brought you.

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    ExistingGame = False
    pygame.display.set_caption('Medieval Fuzzy Logic Chess')
    game_state = GameState.Home
    while True:
        #Quit Gamestate
        if game_state == GameState.Quit:
            pygame.quit()
            return
        #Homescreen GameState
        #remove_highlights()
        if game_state == GameState.Home:
            game_state = MenuScene(screen)
        #play Game
        if (game_state == GameState.AiPlay):
            game_state = aigame(screen)

        #remove_highlights()
        if (game_state == GameState.Play) and (ExistingGame):
            print('playing game')
            game_state = playgame(screen)
        elif (game_state == GameState.Play) and not (ExistingGame):
            print('No Game exists yet')
            game_state = GameState.NewOrLoad

        if game_state == GameState.NewOrLoad:
            game_state = NewOrLoadScene(screen, ExistingGame)

        if game_state == GameState.NewGame:
            clear_board()
            create_board()
            reset_turn()
            ExistingGame = True
            game_state = playgame(screen)

        #Win Game
        #remove_highlights()
        if game_state == GameState.Win:
            ExistingGame = False
            game_state = winLossScreen(screen, True)
        #Lose Game
        if game_state == GameState.Loss:
            ExistingGame = False
            game_state = winLossScreen(screen, False)
            #game_state = playgame(screen)
        if game_state == GameState.Escape:
            game_state = escapeScene(screen)

#---------GAME SAVE---------------
        if game_state == GameState.Save1 and ExistingGame:
            SaveGame(1)
            game_state = escapeScene(screen)
        if game_state == GameState.Save2 and ExistingGame:
            SaveGame(2)
            game_state = escapeScene(screen)
        if game_state == GameState.Save3 and ExistingGame:
            SaveGame(3)
            game_state = escapeScene(screen)
# ---------GAME LOAD---------------
        if game_state == GameState.Load1:
            ExistingGame = True
            LoadGame(1)
            update_display(screen)
            game_state = playgame(screen)
        if game_state == GameState.Load2:
            ExistingGame = True
            LoadGame(2)
            update_display(screen)
            game_state = playgame(screen)
        if game_state == GameState.Load3:
            ExistingGame = True
            LoadGame(3)
            update_display(screen)
            game_state = playgame(screen)

#-----------START RULES PAGEE STUFF ------------------
        #Rules Page
        if game_state == GameState.Rules:
            game_state = RulesPageScene(screen)
        #How To Play
        if game_state == GameState.HowTo:
            game_state = HowToPlayScene(screen)
        #Pieces
        if game_state == GameState.Pieces:
            game_state = PiecesScene(screen)
        #Pawn tab
        if game_state == GameState.Pawn:
            game_state = PawnScene(screen)
        #Rook Tab
        if game_state == GameState.Rook:
            game_state = RookScene(screen)
        #Knight Tab
        if game_state == GameState.Knight:
            game_state = KnightScene(screen)
        #Queen Tab
        if game_state == GameState.Queen:
            game_state = QueenScene(screen)
        #Bishop Tab
        if game_state == GameState.Bishop:
            game_state = BishopScene(screen)
        #King Tab
        if game_state == GameState.King:
            game_state = KingScene(screen)
#------------START GAME BUTTON STUFF -----------------
        if game_state == GameState.Delegate:
            #add code to do something here
            print('Deligation selected.')
            #delegation_mode = True
            game_state = playgame(screen)
        if game_state == GameState.EndTurn:
            #add code to do something
            turnChange()
            reset_turn()
            game_state = playgame(screen)

main()

