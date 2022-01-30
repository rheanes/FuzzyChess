import common as cm
import ScreenGUI as sg
import pygame
import sys
def rulespage(screen):
    HeaderText = cm.font.render("RULES PAGE", True, cm.WHITE)
    Home_Button = sg.button(pos=(cm.WIDTH - 10, cm.HEIGHT - 10), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                         text="Objectives", action=GameState.Title)
    Obj_Tab = sg.button(pos=(cm.WIDTH/6, cm.HEIGHT/8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                     text="Objectives", action = GameState.Objectives)
    Rule_Tab = sg.button(pos=(cm.WIDTH/2, cm.HEIGHT/8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                      text="Rules", action = GameState.Rules)
    Pieces_Tab = sg.button(pos=(5*cm.WIDTH/6, cm.HEIGHT/8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                        text="Pieces", action = GameState.Pieces)
    buttons = [Obj_Tab, Rule_Tab, Pieces_Tab]

    while True:
        screen.fill(cm.blackish)
        screen.blit(HeaderText, (cm.WIDTH / 2 , 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_up = True
        screen.fill(cm.WHITE)

        for tab in tabs:
            ui_action = sg.button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            tab.draw(screen)

        pygame.display.flip()


def ObjectiveTab(screen):
    HeaderText = cm.font.render("RULES PAGE", True, cm.WHITE)
    Home_Button = sg.button(pos=(cm.WIDTH - 10, cm.HEIGHT - 10), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                         text="Objectives", action=GameState.Title)
    Obj_Tab = sg.button(pos=(cm.WIDTH / 6, cm.HEIGHT / 8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                     text="Objectives", action=GameState.Objectives)
    Rule_Tab = sg.button(pos=(cm.WIDTH / 2, cm.HEIGHT / 8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                      text="Rules", action=GameState.Rules)
    Pieces_Tab = sg.button(pos=(5 * cm.WIDTH / 6, cm.HEIGHT / 8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                        text="Pieces", action=GameState.Pieces)
    buttons = [Home_Button, Obj_Tab, Rule_Tab, Pieces_Tab]
    ObjectiveText = "This is the text for our objectives."
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(cm.blackish)
        screen.blit(HeaderText, (cm.WIDTH / 2, 0))
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)
        #TODO WRITE OBJECTIVE TEXT TO SCREEN
        pygame.display.flip()

def RulesTab(screen):
    HeaderText = cm.font.render("RULES PAGE", True, cm.WHITE)
    Home_Button = sg.button(pos=(cm.WIDTH - 10, cm.HEIGHT - 10), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                         text="Objectives", action=GameState.Title)
    Obj_Tab = sg.button(pos=(cm.WIDTH / 6, cm.HEIGHT / 8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                     text="Objectives", action=GameState.Objectives)
    Rule_Tab = sg.button(pos=(cm.WIDTH / 2, cm.HEIGHT / 8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                      text="Rules", action=GameState.Rules)
    Pieces_Tab = sg.button(pos=(5 * cm.WIDTH / 6, cm.HEIGHT / 8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                        text="Pieces", action=GameState.Pieces)
    buttons = [Obj_Tab, Rule_Tab, Pieces_Tab]
    RulesText = "This is the text for the rules"
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(cm.blackish)
        screen.blit(HeaderText, (cm.WIDTH / 2, 0))
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)
        #TODO WRITE OBJECTIVE TEXT TO SCREEN
        pygame.display.flip()
def PiecesTab():
    HeaderText = cm.font.render("RULES PAGE", True, cm.WHITE)
    Home_Button = sg.button(pos=(cm.WIDTH - 10, cm.HEIGHT - 10), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                         text="Objectives", action=GameState.Title)
    Obj_Tab = sg.button(pos=(cm.WIDTH / 6, cm.HEIGHT / 8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                     text="Objectives", action=GameState.Objectives)
    Rule_Tab = sg.button(pos=(cm.WIDTH / 2, cm.HEIGHT / 8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                      text="Rules", action=GameState.Rules)
    Pieces_Tab = sg.button(pos=(5 * cm.WIDTH / 6, cm.HEIGHT / 8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                        text="Pieces", action=GameState.Pieces)
    Pawn_Button = sg.button(pos=(cm.WIDTH/6, cm.HEIGHT/2), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                         text="Pawn", action = GameState.Pawn_Des)
    Rook_Button = sg.button(pos=( cm.WIDTH/2, cm.HEIGHT/2), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                     text="Rook", action=GameState.Rook_Des)
    Knight_Button = sg.button(pos=(5 * cm.WIDTH / 6, cm.HEIGHT/2), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                     text="Knight", action=GameState.Knight_Des)
    Queen_Button = sg.button(pos=(cm.WIDTH / 6, 2*cm.HEIGHT/3), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                     text="Queen", action=GameState.Queen_Des)
    Bishop_Button = sg.button(pos=(cm.WIDTH / 2, 2*cm.HEIGHT/3), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                     text="Bishop", action=GameState.Bishop_Des)
    King_Button = sg.button(pos=(5 * cm.WIDTH / 6, 2*cm.HEIGHT/3), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                     text="King", action=GameState.King_Des)
    buttons = [Obj_Tab, Rule_Tab, Pieces_Tab, Pawn_Button, Rook_Button, Knight_Button,
               Queen_Button, Bishop_Button, King_Button]
    #images and text for pieces
    pawn = sg.Element("./Images/blue_pawn.png", (Pawn_Button.pos[0] , Pawn_Button.pos[1]+ 20))
    knight = sg.Element("./Images/blue_knight.png", (Knight_Button.pos[0] , Knight_Button.pos[1]+ 20))
    bishop = sg.Element("./Images/blue_bishop.png", (Bishop_Button.pos[0] , Bishop_Button.pos[1]+ 20))
    queen = sg.Element("./Images/blue_queen.png", (Queen_Button.pos[0] , Queen_Button.pos[1]+ 20))
    king = sg.Element("./Images/blue_king.png", (King_Button.pos[0] , King_Button.pos[1]+ 20))
    rook = sg.Element("./Images/blue_rook.png", (Rook_Button.pos[0] , Rook_Button.pos[1]+ 20))
    images = [pawn, knight, bishop, queen, king, rook]
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(cm.blackish)
        screen.blit(HeaderText, (cm.WIDTH / 2, 0))
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)
        for image in images:
            image.draw(screen)
        #TODO WRITE OBJECTIVE TEXT TO SCREEN
        pygame.display.flip()