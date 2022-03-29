from guielements import *

from GameScene import playgame, delegation_mode, turnChange, create_board, reset_turn
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
from board import remove_highlights

#pygame.mixer.music.load("Ciara's First Beat.mp3")
#pygame.mixer.music.play(-1)

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
        #remove_highlights()
        if game_state == GameState.Play:
            print('playing game')
            game_state == playgame(screen)

        if game_state == GameState.NewOrLoad:
            game_state = NewOrLoadScene(screen)

        if game_state == GameState.NewGame:
            reset_turn()
            clear_board()
            create_board()
            game_state = playgame(screen)

        #Win Game
        #remove_highlights()
        if game_state == GameState.Win:
            game_state = winLossScreen(screen, True)
            #game_state = playgame(screen)
        #Lose Game (ALSO OCCURS ON RESIGN)
        if game_state == GameState.Loss:
            #remove_highlights()
            game_state = winLossScreen(screen, False)
            #game_state = playgame(screen)
        if game_state == GameState.Escape:
            game_state = escapeScene(screen)

#---------GAME SAVE---------------
        if game_state == GameState.Save1:
            SaveGame(1)
            game_state = playgame(screen)
        if game_state == GameState.Save2:
            SaveGame(2)
            game_state = playgame(screen)
        if game_state == GameState.Save3:
            SaveGame(3)
            game_state = playgame(screen)
# ---------GAME LOAD---------------
        if game_state == GameState.Load1:
            LoadGame(1)
            game_state = playgame(screen)
        if game_state == GameState.Load2:
            LoadGame(2)
            game_state = playgame(screen)
        if game_state == GameState.Load3:
            LoadGame(3)
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
            print('EndTurn selected.')
            game_state = playgame(screen)

main()

