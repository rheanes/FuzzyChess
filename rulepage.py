from guielements import *
def rulespage(screen):
    Home_Button = button(pos=(cm.WIDTH / 2, 0.2 * cm.HEIGHT), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                         text="Return to Homescreen")
    Obj_Tab = button(pos=(cm.WIDTH / 6, cm.HEIGHT / 8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                     text="Objectives")
    Rule_Tab = button(pos=(cm.WIDTH / 2, cm.HEIGHT / 8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                      text="Rules")
    Pieces_Tab = button(pos=(5 * cm.WIDTH / 6, cm.HEIGHT / 8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                        text="Pieces")
    tabs = [Home_Button, Obj_Tab, Rule_Tab, Pieces_Tab]
    ObjectiveTab(screen, tabs)


def ObjectiveTab(screen, tabs):
    HeaderText = cm.font.render("Objectives", True, cm.BLACK)
    ObjectiveText = ["Much like normal chess, the goal of fuzzy logic ",
                     "chess is to capture the enemy's king. However, ",
                     "there are no checks or checkmates and capturing",
                     "the king is like capturing any other piece."]
    text_label, text_pos = create_multiline_text(ObjectiveText, cm.font, cm.WIDTH * 0.05, cm.HEIGHT * 0.35)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    return
                if tabs[1].selected:
                    ObjectiveTab(screen, tabs)
                if tabs[2].selected:
                    RulesTab(screen, tabs)
                if tabs[3].selected:
                    PiecesTab(screen, tabs)
        screen.fill(cm.WHITE)
        screen.blit(HeaderText, (cm.WIDTH * 0.40, cm.HEIGHT / 4))
        # loops through text list and blits each line to the screen
        for line in range(len(text_label)):
            screen.blit(text_label[line], (text_pos[0], text_pos[1] + (line * 30) + (5 * line)))
        for tab in tabs:
            tab.draw(screen)
            tab.moused_over(pygame.mouse.get_pos())
        pygame.display.flip()


def RulesTab(screen, tabs):
    HeaderText = cm.font.render("RULES PAGE", True, cm.BLACK)
    RulesText = ["FuzzyChess is played on a chessboard with standard chess pieces, but the rules are ",
                 "different. The pieces are split into three different corps led by the king and two bishops.",
                 "Each player can make up to three actions per turn, one with each corps. In this version of",
                 "chess, attacking and moving are separate actions so a single piece cannot both move and ",
                 "attack, with the only exceptions being the knights. When a piece tries to capture another,",
                 "a die must be rolled to determine if the capture is a success. If successful, the capturing ",
                 "piece moves to the square of the captured piece. If failed, the capturing piece remains in ",
                 "its original position.", " ",
                 "The three corps are the left, right, and center corps. The left three pawns, the left knight",
                 ",and the left bishop make up the left corps; the right three pawns, the right knight, and ",
                 "the right bishop make up the right corps; the king, the queen, the two middle pawns, and ",
                 "the rooks make up the center corps. As mentioned before, the king and two bishops are the",
                 "commanders of these corps. The commanders can either issue commands to their troops or ",
                 "make an action themselves, but if a command is issued to a troop, the commander may",
                 "also move one square in any direction.  "]
    text_label, text_pos = create_multiline_text(RulesText, cm.rulesfont, cm.WIDTH * 0.05, cm.HEIGHT * 0.35)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    return
                if tabs[1].selected:
                    ObjectiveTab(screen, tabs)
                if tabs[2].selected:
                    RulesTab(screen, tabs)
                if tabs[3].selected:
                    PiecesTab(screen, tabs)
            screen.fill(cm.WHITE)
            screen.blit(HeaderText, (cm.WIDTH * 0.4, cm.HEIGHT / 4))
            for line in range(len(text_label)):
                screen.blit(text_label[line], (text_pos[0], text_pos[1] + (line * 18) + (10 * line)))
            for tab in tabs:
                tab.draw(screen)
                tab.moused_over(pygame.mouse.get_pos())
            pygame.display.flip()


def PiecesTab(screen, tabs):
    positions = [(cm.WIDTH / 6, cm.HEIGHT / 2), (cm.WIDTH / 2, cm.HEIGHT / 2),
                 (5 * cm.WIDTH / 6, cm.HEIGHT / 2), (cm.WIDTH / 6, 7 * cm.HEIGHT / 8),
                 (cm.WIDTH / 2, 7 * cm.HEIGHT / 8), (5 * cm.WIDTH / 6, 7 * cm.HEIGHT / 8)]
    # HeaderText = cm.font.render("RULES PAGE", True, cm.BLACK)
    Pawn_Button = button(pos=(positions[0]), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                         text="Pawn")
    Rook_Button = button(pos=(positions[1]), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                         text="Rook")
    Knight_Button = button(pos=(positions[2]), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                           text="Knight")
    Queen_Button = button(pos=(positions[3]), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                          text="Queen")
    Bishop_Button = button(pos=(positions[4]), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                           text="Bishop")
    King_Button = button(pos=(positions[5]), font_size=50, txt_col=cm.BLACK,
                         bg_col=cm.buttoncolor,
                         text="King")
    buttons = [Pawn_Button, Rook_Button, Knight_Button, Queen_Button, Bishop_Button, King_Button]
    # images and text for pieces
    pawn = Element("./Images/blue_pawn.png", (positions[0][0], positions[0][1] - 20))
    rook = Element("./Images/blue_rook.png", (positions[1][0], positions[1][1] - 20))
    knight = Element("./Images/blue_knight.png", (positions[2][0], positions[2][1] - 20))
    queen = Element("./Images/blue_queen.png", (positions[3][0], positions[3][1] - 20))
    bishop = Element("./Images/blue_bishop.png", (positions[4][0], positions[4][1] - 20))
    king = Element("./Images/blue_king.png", (positions[5][0], positions[5][1] - 20))
    images = [pawn, rook, knight, queen, bishop, king]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    return
                if tabs[1].selected:
                    ObjectiveTab(screen, tabs)
                if tabs[2].selected:
                    RulesTab(screen, tabs)
                if tabs[3].selected:
                    PiecesTab(screen, tabs)
                if buttons[0].selected:
                    pawnPage(screen, tabs)
                if buttons[1].selected:
                    rookPage(screen, tabs)
                if buttons[2].selected:
                    knightPage(screen, tabs)
                if buttons[3].selected:
                    queenPage(screen, tabs)
                if buttons[4].selected:
                    bishopPage(screen, tabs)
                if buttons[5].selected:
                    kingPage(screen, tabs)
            screen.fill(cm.WHITE)
            # screen.blit(HeaderText, (cm.WIDTH / 2, 0))
            for tab in tabs:
                tab.draw(screen)
                tab.moused_over(pygame.mouse.get_pos())
            for img in images:
                img.draw(screen)
            for b in buttons:
                b.draw(screen)
                b.moused_over(pygame.mouse.get_pos())

            pygame.display.flip()


def pawnPage(screen, tabs):
    HeaderText = cm.font.render("The Pawn", True, cm.BLACK)
    PieceDes = ["The basic infantry and usually considered cannon ",
                "fodder, they can only move one square at a time",
                "and may only move forward or forward diagonally, ",
                "they can only attack in the same way they move, when",
                "they reach the other side, they do not gain a",
                "promotion like in traditional chess."]
    text_label, text_pos = create_multiline_text(PieceDes, cm.font, cm.WIDTH * 0.05, cm.HEIGHT * 0.60)
    positions = [(cm.WIDTH / 6, 3 / 8 * cm.HEIGHT), (cm.WIDTH / 3, 3 / 8 * cm.HEIGHT),
                 (cm.WIDTH / 2, 3 / 8 * cm.HEIGHT),
                 (2 / 3 * cm.WIDTH, 3 / 8 * cm.HEIGHT), (5 / 6 * cm.WIDTH, 3 / 8 * cm.HEIGHT),
                 (cm.WIDTH, 3 / 8 * cm.HEIGHT)]
    img1 = Element("./Images/blue_pawn.png", (positions[0][0], positions[0][1]))
    img2 = Element("./Images/purple_pawn.png", (positions[1][0], positions[1][1]))
    img3 = Element("./Images/green_pawn.png", (positions[2][0], positions[2][1]))
    img4 = Element("./Images/red_pawn.png", (positions[3][0], positions[3][1]))
    img5 = Element("./Images/orange_pawn.png", (positions[4][0], positions[4][1]))
    img6 = Element("./Images/yellow_pawn.png", (positions[5][0], positions[5][1]))
    imgs = [img1, img2, img3, img4, img5, img6]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    return
                if tabs[1].selected:
                    ObjectiveTab(screen, tabs)
                if tabs[2].selected:
                    RulesTab(screen, tabs)
                if tabs[3].selected:
                    PiecesTab(screen, tabs)
        screen.fill(cm.WHITE)
        screen.blit(HeaderText, (cm.WIDTH * 0.4, cm.HEIGHT * 0.55))
        for tab in tabs:
            tab.draw(screen)
            tab.moused_over(pygame.mouse.get_pos())
        for img in imgs:
            img.draw(screen)
        for line in range(len(text_label)):
            screen.blit(text_label[line], (text_pos[0], text_pos[1] + (line * 18) + (10 * line)))

        pygame.display.flip()


def rookPage(screen, tabs):
    HeaderText = cm.font.render("The Rook", True, cm.BLACK)
    PieceDes = ["The archers, they provide long range support, they "
        , "can move up to two squares in any direction and do "
        , "not have to move in a straight line, they can make an  "
        , "attack in any direction up to three squares away,  "
        , "they do this by shooting over any squares between "
        , "them and their target  so only the target is hit."]
    text_label, text_pos = create_multiline_text(PieceDes, cm.font, cm.WIDTH * 0.05, cm.HEIGHT * 0.60)
    positions = [(cm.WIDTH / 6, 3 / 8 * cm.HEIGHT), (cm.WIDTH / 3, 3 / 8 * cm.HEIGHT),
                 (cm.WIDTH / 2, 3 / 8 * cm.HEIGHT),
                 (2 / 3 * cm.WIDTH, 3 / 8 * cm.HEIGHT), (5 / 6 * cm.WIDTH, 3 / 8 * cm.HEIGHT),
                 (cm.WIDTH, 3 / 8 * cm.HEIGHT)]
    img1 = Element("./Images/blue_rook.png", (positions[0][0], positions[0][1]))
    img2 = Element("./Images/purple_rook.png", (positions[1][0], positions[1][1]))
    img3 = Element("./Images/green_rook.png", (positions[2][0], positions[2][1]))
    img4 = Element("./Images/red_rook.png", (positions[3][0], positions[3][1]))
    img5 = Element("./Images/orange_rook.png", (positions[4][0], positions[4][1]))
    img6 = Element("./Images/yellow_rook.png", (positions[5][0], positions[5][1]))
    imgs = [img1, img2, img3, img4, img5, img6]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    return
                if tabs[1].selected:
                    ObjectiveTab(screen, tabs)
                if tabs[2].selected:
                    RulesTab(screen, tabs)
                if tabs[3].selected:
                    PiecesTab(screen, tabs)
        screen.fill(cm.WHITE)
        screen.blit(HeaderText, (cm.WIDTH * 0.4, cm.HEIGHT * 0.55))
        for tab in tabs:
            tab.draw(screen)
            tab.moused_over(pygame.mouse.get_pos())
        for img in imgs:
            img.draw(screen)
        for line in range(len(text_label)):
            screen.blit(text_label[line], (text_pos[0], text_pos[1] + (line * 18) + (10 * line)))
        pygame.display.flip()


def knightPage(screen, tabs):
    HeaderText = cm.font.render("The Knight", True, cm.BLACK)
    PieceDes = ["The mounted attackers charging into battle, they can "
        , "move up to four squares in any direction and do not "
        , "have to move in a straight line, they can attack any  "
        , "adjacent square, they also have the ability to move and "
        , "attack in the same turn, this counts as an ambush and "
        , "when capturing an enemy after moving they add one to  "
        , "the die roll (note: when the knight makes the attack, their "
        , "turn is over, you must move, then attack)."]
    text_label, text_pos = create_multiline_text(PieceDes, cm.font, cm.WIDTH * 0.05, cm.HEIGHT * 0.60)
    positions = [(cm.WIDTH / 6, 3 / 8 * cm.HEIGHT), (cm.WIDTH / 3, 3 / 8 * cm.HEIGHT),
                 (cm.WIDTH / 2, 3 / 8 * cm.HEIGHT),
                 (2 / 3 * cm.WIDTH, 3 / 8 * cm.HEIGHT), (5 / 6 * cm.WIDTH, 3 / 8 * cm.HEIGHT),
                 (cm.WIDTH, 3 / 8 * cm.HEIGHT)]
    img1 = Element("./Images/blue_knight.png", (positions[0][0], positions[0][1]))
    img2 = Element("./Images/purple_knight.png", (positions[1][0], positions[1][1]))
    img3 = Element("./Images/green_knight.png", (positions[2][0], positions[2][1]))
    img4 = Element("./Images/red_knight.png", (positions[3][0], positions[3][1]))
    img5 = Element("./Images/orange_knight.png", (positions[4][0], positions[4][1]))
    img6 = Element("./Images/yellow_knight.png", (positions[5][0], positions[5][1]))
    imgs = [img1, img2, img3, img4, img5, img6]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    return
                if tabs[1].selected:
                    ObjectiveTab(screen, tabs)
                if tabs[2].selected:
                    RulesTab(screen, tabs)
                if tabs[3].selected:
                    PiecesTab(screen, tabs)
        screen.fill(cm.WHITE)
        screen.blit(HeaderText, (cm.WIDTH * 0.4, cm.HEIGHT * 0.55))
        for tab in tabs:
            tab.draw(screen)
            tab.moused_over(pygame.mouse.get_pos())
        for img in imgs:
            img.draw(screen)
        for line in range(len(text_label)):
            screen.blit(text_label[line], (text_pos[0], text_pos[1] + (line * 18) + (10 * line)))
        pygame.display.flip()


def queenPage(screen, tabs):
    HeaderText = cm.font.render("The Queen", True, cm.BLACK)
    PieceDes = ["The king’s right (or left) hand, she can move up to three "
        , "squares in any direction and does not have to move in a "
        , "straight line, she can also attack any adjacent squares."]
    text_label, text_pos = create_multiline_text(PieceDes, cm.font, cm.WIDTH * 0.05, cm.HEIGHT * 0.60)
    positions = [(cm.WIDTH / 4, 3 / 8 * cm.HEIGHT), (cm.WIDTH * 3 / 4, 3 / 8 * cm.HEIGHT)]
    img1 = Element("./Images/blue_queen.png", (positions[0][0], positions[0][1]))
    img2 = Element("./Images/red_queen.png", (positions[1][0], positions[1][1]))
    imgs = [img1, img2]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    return
                if tabs[1].selected:
                    ObjectiveTab(screen, tabs)
                if tabs[2].selected:
                    RulesTab(screen, tabs)
                if tabs[3].selected:
                    PiecesTab(screen, tabs)
        screen.fill(cm.WHITE)
        screen.blit(HeaderText, (cm.WIDTH * 0.4, cm.HEIGHT * 0.55))
        for tab in tabs:
            tab.draw(screen)
            tab.moused_over(pygame.mouse.get_pos())
        for img in imgs:
            img.draw(screen)
        for line in range(len(text_label)):
            screen.blit(text_label[line], (text_pos[0], text_pos[1] + (line * 18) + (10 * line)))
        pygame.display.flip()


def bishopPage(screen, tabs):
    HeaderText = cm.font.render("The Bishop", True, cm.BLACK)
    PieceDes = ["The king’s trusted advisors, if they are captured, then"
        , "the pieces under their command fall to the king’s "
        , "command and that corps’ action is lost for the remainder  "
        , "of the game, they can move up to two squares  "
        , "in any direction and do not have to move in a straight "
        , "line, they can attack any adjacent square."]
    text_label, text_pos = create_multiline_text(PieceDes, cm.font, cm.WIDTH * 0.05, cm.HEIGHT * 0.60)
    positions = [(cm.WIDTH / 3, 3 / 8 * cm.HEIGHT), (cm.WIDTH / 2, 3 / 8 * cm.HEIGHT),
                 (cm.WIDTH * 2 / 3, 3 / 8 * cm.HEIGHT), (5 / 6 * cm.WIDTH, 3 / 8 * cm.HEIGHT)]
    img1 = Element("./Images/green_bishop.png", (positions[0][0], positions[0][1]))
    img2 = Element("./Images/purple_bishop.png", (positions[1][0], positions[1][1]))
    img3 = Element("./Images/orange_bishop.png", (positions[2][0], positions[2][1]))
    img4 = Element("./Images/yellow_bishop.png", (positions[3][0], positions[3][1]))
    imgs = [img1, img2, img3, img4]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    return
                if tabs[1].selected:
                    ObjectiveTab(screen, tabs)
                if tabs[2].selected:
                    RulesTab(screen, tabs)
                if tabs[3].selected:
                    PiecesTab(screen, tabs)
        screen.fill(cm.WHITE)
        screen.blit(HeaderText, (cm.WIDTH * 0.4, cm.HEIGHT * 0.55))
        for tab in tabs:
            tab.draw(screen)
            tab.moused_over(pygame.mouse.get_pos())
        for img in imgs:
            img.draw(screen)
        for line in range(len(text_label)):
            screen.blit(text_label[line], (text_pos[0], text_pos[1] + (line * 18) + (10 * line)))
        pygame.display.flip()


def kingPage(screen, tabs):
    HeaderText = cm.font.render("The King", True, cm.BLACK)
    PieceDes = ["if this piece is captured you lose, the leader of the army"
        , "and commander of the center corps, can move up to "
        , "three squares in any direction and does not have to  "
        , "move in a straight line, can attack any adjacent square, "
        , "can delegate pieces in his corps to another corps or ",
                "pull pieces from the other corps into his own (this counts as "
        , "this corps action)."]
    text_label, text_pos = create_multiline_text(PieceDes, cm.font, cm.WIDTH * 0.05, cm.HEIGHT * 0.60)
    positions = [(cm.WIDTH / 4, 3 / 8 * cm.HEIGHT), (cm.WIDTH * 3 / 4, 3 / 8 * cm.HEIGHT)]
    img1 = Element("./Images/blue_king.png", (positions[0][0], positions[0][1]))
    img2 = Element("./Images/red_king.png", (positions[1][0], positions[1][1]))
    imgs = [img1, img2]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    return
                if tabs[1].selected:
                    ObjectiveTab(screen, tabs)
                if tabs[2].selected:
                    RulesTab(screen, tabs)
                if tabs[3].selected:
                    PiecesTab(screen, tabs)
        screen.fill(cm.WHITE)
        screen.blit(HeaderText, (cm.WIDTH * 0.4, cm.HEIGHT * 0.55))
        for tab in tabs:
            tab.draw(screen)
            tab.moused_over(pygame.mouse.get_pos())
        for img in imgs:
            img.draw(screen)
        for line in range(len(text_label)):
            screen.blit(text_label[line], (text_pos[0], text_pos[1] + (line * 18) + (10 * line)))
        pygame.display.flip()

