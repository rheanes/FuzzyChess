from GameScene import *
def aigame(screen):
    #Button handles the free move commanders can make each turn
    Command_Move_Button = CommFreeMove(pos=(WIDTH - 300, 200),
                                     font_size=40,
                                     txt_col=BLACK,
                                     bg_col=buttoncolor,
                                     text="Com. Free Move",
                                     bg_hover=buttonhover,
                                     action=GameState.Play)

    Delegate_Button = DelegateButton(pos=(WIDTH - 300, 275),
                                     font_size=50,
                                     txt_col=BLACK,
                                     bg_col=buttoncolor,
                                     text="Delegate",
                                     bg_hover=buttonhover,
                                     action=GameState.Play)

    Recall_Button = RecallButton(pos=(WIDTH - 300, 350),
                           font_size=50,
                           txt_col=BLACK,
                           bg_col=buttoncolor,
                           text="Recall",
                           bg_hover=buttonhover,
                           action=GameState.Play)
    End_Turn_Button = button(pos=(WIDTH - 300, 425),
                             font_size=50,
                             txt_col=BLACK,
                             bg_col=buttoncolor,
                             text="End Turn",
                             bg_hover=buttonhover,
                             action=GameState.EndTurn)


    Action_Counter = Action_Counttxt(pos=(WIDTH - 300, 125),
                                     font_size=50,
                                     txt_col=BLACK,
                                     bg_col=buttoncolor,
                                     text="Action Count: ",
                                     bg_hover=buttonhover,
                                     action=GameState.Play)

    Current_turn = WhosTurn(pos=(WIDTH - 300, 50),
                            font_size=50,
                            txt_col=BLACK,
                            bg_col=buttoncolor,
                            text="Current Turn: AI",
                            bg_hover=buttonhover,
                            action=GameState.Play)

    Bone_Pile = BoneP(pos=(WIDTH - 1075, 650),
                            font_size=50,
                            txt_col=BLACK,
                            bg_col=buttoncolor,
                            text="Bone Pile",
                            bg_hover=buttonhover,
                            action=GameState.Play)

    buttons = [Delegate_Button, End_Turn_Button, Recall_Button,
               Action_Counter, Current_turn, Bone_Pile, Command_Move_Button]

    current_square = None
    global action_count
    global turn
    delegated_pieces = []
    global delegation_mode
    global recall_mode
    global commander
    global blue_commander
    global red_commander
    captured_pieces = []
    global deployed_team
    action_limit = 3
    knight_special_turn = False
    human_team = [Team.GREEN, Team.BLUE, Team.PURPLE]

    ai = AI

    while True:
        mouse_down = False
        pygame.mouse.get_pressed()
        # print('Delegation: ', Delegate_Button.selected)
        # print('Delegation remain selected: ', Delegate_Button.remain_selected)
        # print('Delegation Mode: ', delegation_mode)
        # print('action count', action_count)
        Action_Counter.text = 'Action Count: ' + str(action_count)

        if action_count <= 0 and not turn:
            turnChange()
            reset_turn()

        if turn:
            # print('human turn')
            # print('enter pygame events')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif(event.type == KEYDOWN):
                    if event.key == K_ESCAPE:
                        return GameState.Escape
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mouse_down = True

                    x, y = pygame.mouse.get_pos()
                    # if you dont click on the game board
                    if x >= GAME_WIDTH or y >= GAME_WIDTH:
                        if End_Turn_Button.selected:
                            turnChange()
                            reset_turn()

                    # if you do click on the game board
                    else:
                        row, col = find_square_coordinates((x, y))
                        # print('row ', row, ' col ', col)
                        chosen_square = board[row][col]  # refers to the square clicked by the mouse
                        """ current causes issues
                        # prevents clicking on enemy pieces
                        if (chosen_square.piece.team in enemies) and chosen_square.piece:
                            pass
                        else:
                        """

                        if delegation_mode and human_piece_delegated is not True and checkCommanderTurn(Team.BLUE):
                                result = delegate(chosen_square)
                                if result is not None:
                                    delegated_pieces.append(result)

                        elif recall_mode and human_piece_delegated is not True and checkCommanderTurn(Team.BLUE):
                            recall(chosen_square)

                        #Defines the free movement the commander can make without expending its corp turn
                        #This only occurs if the button is pressed
                        else:
                            global commMoveMode
                            # if chosen_square.piece.team in human_team:
                            # conditions for selected_square
                            if current_square is None:
                                if chosen_square.piece is None:
                                    remove_highlights()
                                    pass

                                elif commMoveMode:
                                    if (commAuth(chosen_square)):
                                        current_square = chosen_square
                                        commMove(chosen_square)
                                    else:
                                        commMoveMode = False

                                elif (checkCommanderTurn(chosen_square.piece.team) or chosen_square.piece.type is Type.KNIGHT) and (chosen_square.piece.team not in enemies[Team.BLUE]):
                                    if chosen_square.piece.type is Type.KNIGHT:
                                        if knight_special_turn and adjacent_enemies((chosen_square.row, chosen_square.col), chosen_square.piece.team):
                                            if(chosen_square.piece.team is Team.BLUE):
                                                if(blue_commander.has_moved):
                                                    current_square = chosen_square
                                                    knightAttack(chosen_square)
                                            elif(chosen_square.piece.team is Team.GREEN):
                                                if(green_commander.has_moved):
                                                    current_square = chosen_square
                                                    knightAttack(chosen_square)
                                            elif(chosen_square.piece.team is Team.PURPLE):
                                                if(purple_commander.has_moved):
                                                    current_square = chosen_square
                                                    knightAttack(chosen_square)
                                        elif knight_special_turn and not adjacent_enemies((chosen_square.row, chosen_square.col), chosen_square.piece.team):
                                            current_square = chosen_square
                                            potential_piece_moves(chosen_square)

                                        elif not knight_special_turn and checkCommanderTurn(chosen_square.piece.team):
                                            current_square = chosen_square
                                            potential_piece_moves(chosen_square)
                                    elif not knight_special_turn or chosen_square.piece.type is not Type.KNIGHT:
                                        current_square = chosen_square
                                        potential_piece_moves(chosen_square)
                                        # if chosen_square.piece is purple_commander.leader:
                                        # print("purple pieces")
                                        # purple_commander.see_pieces

                            else:  # a piece is currently selected
                                """
                                if chosen_square.piece is not None: # clicking alternative piece on your side
                                    remove_highlights()
                                    current_square = chosen_square
                                    potential_piece_moves(chosen_square)
                                """
                                #This check ensures that the chosen corp hasn't worked. If a knight is selected, then
                                #we bypass this condition if the knight's special turn is enabled.
                                if (checkCommanderTurn(current_square.piece.team) or current_square.piece.type is Type.KNIGHT or commMoveMode) and (current_square.piece.team not in enemies[Team.BLUE]):
                                    if (chosen_square.color is WHITE) or (
                                            chosen_square.color is GREY):  # lets you unselect current piece
                                        remove_highlights()
                                        current_square = None
                                        if commMoveMode:
                                            commMoveMode = False

                                    elif knight_special_turn and current_square.piece.type is Type.KNIGHT and adjacent_enemies((current_square.row, current_square.col), current_square.piece.team):
                                        if chosen_square.color is BLACK:
                                            if attack(current_square.piece.type.value,
                                                      chosen_square.piece.type.value, checkCommanderHasMoved(current_square.piece.team)) is True:
                                                captured_pieces.append(chosen_square.piece)
                                                end_commander_turn(chosen_square.piece.team)

                                                if chosen_square.piece.type is Type.BISHOP:
                                                    removeCommander(chosen_square.piece.team)
                                                    remove_team(chosen_square.piece.team)
                                                elif (chosen_square.piece.type is Type.KING) and \
                                                        (chosen_square.piece.team is Team.RED):
                                                    return GameState.Win

                                                chosen_square.piece = None
                                                move_piece(current_square, chosen_square)
                                                current_square = None
                                                action_count -= 1
                                                remove_highlights()
                                                if (chosen_square.piece.team is Team.BLUE):
                                                    blue_commander.has_moved = False
                                                elif (chosen_square.piece.team is Team.GREEN):
                                                    green_commander.has_moved = False
                                                elif (chosen_square.piece.team is Team.PURPLE):
                                                    purple_commander.has_moved = False
                                            else:
                                                end_commander_turn(current_square.piece.team)
                                                chosen_square = None
                                                current_square = None
                                                remove_highlights()
                                                action_count -= 1
                                                if (chosen_square.piece.team is Team.BLUE):
                                                    blue_commander.has_moved = False
                                                elif (chosen_square.piece.team is Team.GREEN):
                                                    green_commander.has_moved = False
                                                elif (chosen_square.piece.team is Team.PURPLE):
                                                    purple_commander.has_moved = False


                                    elif (chosen_square.color is BLUE) and \
                                            (chosen_square.piece is None):  # deals with movement

                                        """
                                            current_square = None
                                            remove_highlights()
                                            move_piece(current_square, chosen_square)
                                            action_count -= 1
                                        else:
                                        """
                                        if current_square.piece.type == Type.KNIGHT and adjacent_enemies((chosen_square.row, chosen_square.col), current_square.piece.team):
                                            # action_count -= 1
                                            # print('action count decreased')
                                            knight_team = current_square.piece.team
                                            if knight_team == Team.GREEN:
                                                green_commander.has_moved = True
                                            elif knight_team == Team.PURPLE:
                                                purple_commander.has_moved = True
                                            elif knight_team == Team.BLUE:
                                                blue_commander.has_moved = True
                                            else:
                                                pass
                                            end_commander_turn(current_square.piece.team)
                                            knight_special_turn = True

                                        if not knight_special_turn and not commMoveMode:
                                            end_commander_turn(current_square.piece.team)
                                            action_count -= 1

                                        #Extra check so that the user can choose to not attack with the Knight and make another action
                                        #that affects the turn count
                                        elif knight_special_turn and not commMoveMode and current_square.piece.type != Type.KNIGHT:
                                            end_commander_turn(current_square.piece.team)
                                            action_count -= 1

                                        #We only end turn and reduce action count if we aren't performing a commander move.
                                        #If we are, then we can ignore the above and just set the commanders authority to false
                                        if (commMoveMode):
                                            commMoveMode = False
                                            if current_square.piece.team is Team.BLUE:
                                                blue_commander.authority = False
                                            elif current_square.piece.team is Team.GREEN:
                                                green_commander.authority = False
                                            elif current_square.piece.team is Team.PURPLE:
                                                purple_commander.authority = False
                                        move_piece(current_square, chosen_square)
                                        remove_highlights()
                                        current_square = None

                                    elif (chosen_square.color is BLACK):
                                        if attack(current_square.piece.type.value,
                                                  chosen_square.piece.type.value) is True:
                                            captured_pieces.append(chosen_square.piece)
                                            remove_piece(chosen_square.piece)
                                            end_commander_turn(chosen_square.piece.team)

                                            if chosen_square.piece.type is Type.BISHOP:
                                                #We decrement the counter to ensure the actions done by a human are limited based on the number of commanders we have
                                                removeCommander(chosen_square.piece.team)
                                                remove_team(chosen_square.piece.team)
                                            elif (chosen_square.piece.type is Type.KING) and (
                                                    chosen_square.piece.team is Team.RED):
                                                return GameState.Win
                                            elif (chosen_square.piece.type is Type.KING) and (
                                                    chosen_square.piece.team is Team.BLUE):
                                                return GameState.Loss

                                            chosen_square.piece = None
                                            if (current_square.piece.type is not Type.ROOK):
                                                move_piece(current_square, chosen_square)
                                                end_commander_turn(chosen_square.piece.team)
                                            else:
                                                end_commander_turn(current_square.piece.team)
                                            current_square = None
                                            action_count -= 1
                                            remove_highlights()
                                        else:
                                            remove_highlights()
                                            end_commander_turn(current_square.piece.team)
                                            action_count -= 1
                                            current_square = None
                                else:
                                    remove_highlights()
                                    chosen_square = None
                                    current_square = None
                                    pass
                else:
                    pass
        elif not turn:  # AI starts
            # captured_commander = check_commanders()
            #ai.decision()
            print("Ai Action " + str(action_count))
            # print('hello from computer')
            # after AI is done enable next line
            action_count -= 1

        update_display(screen)
        for b in buttons:
            ui_action = b.moused_over(pygame.mouse.get_pos(), mouse_down)
            if ui_action is not None:
                # if b == Deligate_Button:

                return ui_action
            b.draw(screen)
        pygame.display.flip()
        clock.tick(15)
