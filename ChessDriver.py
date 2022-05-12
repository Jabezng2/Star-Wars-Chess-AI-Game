"""
Main driver file.
Handling user input.
Displaying current GameStatus object.
"""
# Importations
import pygame as p
import ChessEngine, ChessAI, ChessVisual
import sys
from multiprocessing import Process, Queue

class ChessController():
    def __init__(self):
        self.chessVisual = ChessVisual.ChessVisual()
        self.chessVisual.loadImages()
        self.chessModel = ChessEngine.GameState()

    def animateMove(self, move, screen, board, clock):
        """
        Animating a move
        """
        colors = [p.Color("white"), p.Color("gray")]
        d_row = move.end_row - move.start_row
        d_col = move.end_col - move.start_col
        frames_per_square = 7  # frames to move one square aka the speed at which the piece moves
        frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
        for frame in range(frame_count + 1):
            row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
            self.chessVisual.drawBoard(screen)
            self.chessVisual.drawPieces(screen, board)
            # erase the piece moved from its ending square
            color = colors[(move.end_row + move.end_col) % 2]
            end_square = p.Rect(move.end_col * self.chessVisual.SQUARE_SIZE, move.end_row * self.chessVisual.SQUARE_SIZE,
                                self.chessVisual.SQUARE_SIZE, self.chessVisual.SQUARE_SIZE)
            p.draw.rect(screen, color, end_square)
            # draw captured piece onto rectangle
            if move.piece_captured != '--':
                if move.is_enpassant_move:
                    enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                    end_square = p.Rect(move.end_col * self.chessVisual.SQUARE_SIZE, enpassant_row * self.chessVisual.SQUARE_SIZE,
                                        self.chessVisual.SQUARE_SIZE, self.chessVisual.SQUARE_SIZE)
                screen.blit(self.chessVisual.IMAGES[move.piece_captured], end_square)
            # draw moving piece
            screen.blit(self.chessVisual.IMAGES[move.piece_moved], p.Rect(col * self.chessVisual.SQUARE_SIZE,
                                                                                           row * self.chessVisual.SQUARE_SIZE,
                                                                                           self.chessVisual.SQUARE_SIZE,
                                                                                           self.chessVisual.SQUARE_SIZE))
            p.display.flip()
            clock.tick(60)

    def highlightSquares(self, screen, game_state, valid_moves, square_selected):
        """
        Highlight square selected and moves for piece selected.
        """
        if (len(self.chessModel.move_log)) > 0:
            last_move = game_state.move_log[-1]
            s = p.Surface((self.chessVisual.SQUARE_SIZE, self.chessVisual.SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('green'))
            self.chessVisual.screen.blit(s, (last_move.end_col * self.chessVisual.SQUARE_SIZE,
                                             last_move.end_row * self.chessVisual.SQUARE_SIZE))
        if square_selected != ():
            row, col = square_selected
            if game_state.board[row][col][0] == (
                    'w' if game_state.white_to_move else 'b'):  # square_selected is a piece that can be moved
                # highlight selected square
                s = p.Surface((self.chessVisual.SQUARE_SIZE, self.chessVisual.SQUARE_SIZE))
                s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
                s.fill(p.Color('blue'))
                screen.blit(s, (col * self.chessVisual.SQUARE_SIZE, row * self.chessVisual.SQUARE_SIZE))
                # highlight moves from that square
                s.fill(p.Color('yellow'))
                for move in valid_moves:
                    if move.start_row == row and move.start_col == col:
                        self.chessVisual.screen.blit(s, (move.end_col * self.chessVisual.SQUARE_SIZE,
                                                         move.end_row * self.chessVisual.SQUARE_SIZE))

    def drawGameState(self, screen, game_state, valid_moves, square_selected):
        """
        Responsible for all the graphics within current game state.
        """
        self.chessVisual.drawBoard(screen)  # draw squares on the board
        self.highlightSquares(screen, game_state, valid_moves, square_selected)
        self.chessVisual.drawPieces(screen, game_state.board)  # draw pieces on top of those squares

    def drawMoveLog(self, screen, game_state, font):
        """
        Draws the move log.
        """
        move_log_rect = p.Rect(self.chessVisual.BOARD_WIDTH, 0, self.chessVisual.MOVE_LOG_PANEL_WIDTH,
                               self.chessVisual.MOVE_LOG_PANEL_HEIGHT)
        p.draw.rect(screen, p.Color('black'), move_log_rect)
        move_log = game_state.move_log
        move_texts = []
        for i in range(0, len(move_log), 2):
            move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
            if i + 1 < len(move_log):
                move_string += str(move_log[i + 1]) + "  "
            move_texts.append(move_string)

        moves_per_row = 3
        padding = 5
        line_spacing = 2
        text_y = padding
        for i in range(0, len(move_texts), moves_per_row):
            text = ""
            for j in range(moves_per_row):
                if i + j < len(move_texts):
                    text += move_texts[i + j]

            text_object = font.render(text, True, p.Color('white'))
            text_location = move_log_rect.move(padding, text_y)
            screen.blit(text_object, text_location)
            text_y += text_object.get_height() + line_spacing

    def runGame(self, player_one, player_two, windowText):
        """
        The main driver for our code.
        This will handle user input and updating the graphics.
        """
        p.init()
        screen = p.display.set_mode((self.chessVisual.BOARD_WIDTH + self.chessVisual.MOVE_LOG_PANEL_WIDTH,
                                     self.chessVisual.BOARD_HEIGHT))
        clock = p.time.Clock()
        screen.fill(p.Color("white"))
        game_state = ChessEngine.GameState()
        valid_moves = game_state.getValidMoves()
        move_made = False  # flag variable for when a move is made
        p.display.set_caption(windowText)
        animate = False  # flag variable for when we should animate a move
        self.chessVisual.loadImages()  # do this only once before while loop
        running = True
        square_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
        player_clicks = []  # this will keep track of player clicks (two tuples)
        game_over = False
        ai_thinking = False
        move_undone = False
        move_finder_process = None
        move_log_font = p.font.SysFont("Arial", 14, False, False)

        while running:
            human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    sys.exit()
                # mouse handler
                elif e.type == p.MOUSEBUTTONDOWN:
                    if not game_over:
                        location = p.mouse.get_pos()  # (x, y) location of the mouse
                        col = location[0] // self.chessVisual.SQUARE_SIZE
                        row = location[1] // self.chessVisual.SQUARE_SIZE
                        if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                            square_selected = ()  # deselect
                            player_clicks = []  # clear clicks
                        else:
                            square_selected = (row, col)
                            player_clicks.append(square_selected)  # append for both 1st and 2nd click
                        if len(player_clicks) == 2 and human_turn:  # after 2nd click
                            move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    game_state.makeMove(valid_moves[i])
                                    move_made = True
                                    animate = True
                                    square_selected = ()  # reset user clicks
                                    player_clicks = []
                            if not move_made:
                                player_clicks = [square_selected]
                # key handler
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z:  # undo when 'z' is pressed
                        game_state.undoMove()
                        move_made = True
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True
                    if e.key == p.K_r:  # reset the game when 'r' is pressed
                        game_state = ChessEngine.GameState()
                        valid_moves = game_state.getValidMoves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True
            # AI move finder
            if not game_over and not human_turn and not move_undone:
                if not ai_thinking:
                    ai_thinking = True
                    return_queue = Queue()  # used to pass data between threads
                    move_finder_process = Process(target=ChessAI.findBestMove, args=(game_state, valid_moves, return_queue))
                    move_finder_process.start()

                if not move_finder_process.is_alive():
                    ai_move = return_queue.get()
                    if ai_move is None:
                        ai_move = ChessAI.findRandomMove(valid_moves)
                    game_state.makeMove(ai_move)
                    move_made = True
                    animate = True
                    ai_thinking = False

            if move_made:
                if animate:
                    self.animateMove(game_state.move_log[-1], screen, game_state.board, clock)
                valid_moves = game_state.getValidMoves()
                move_made = False
                animate = False
                move_undone = False

            self.drawGameState(screen, game_state, valid_moves, square_selected)

            if not game_over:
                self.drawMoveLog(screen, game_state, move_log_font)

            if game_state.checkmate:
                game_over = True
                if game_state.white_to_move:
                    self.chessVisual.drawEndGameText(screen, "Black wins by checkmate")
                else:
                    self.chessVisual.drawEndGameText(screen, "White wins by checkmate")

            elif game_state.stalemate:
                game_over = True
                self.chessVisual.drawEndGameText(screen, "Stalemate")

            clock.tick(self.chessVisual.MAX_FPS)
            p.display.flip()

    def playGame(self):
        while True:
            self.chessVisual.mainMenu()
            mx, my = p.mouse.get_pos()
            if self.chessVisual.buttons["buttonPlayAsLightSide"].collidepoint((mx, my)):
                if self.chessVisual.click:
                    self.runGame(True, False, "You (LightSide) vs AI (DarkSide)")
            # Settle the color side position hard to play
            if self.chessVisual.buttons["buttonPlayAsDarkSide"].collidepoint((mx, my)):
                if self.chessVisual.click:
                    self.runGame(False, True, "You (DarkSide) vs AI (LightSide)")
            if self.chessVisual.buttons["buttonCredits"].collidepoint((mx, my)):
                if self.chessVisual.click:
                    self.chessVisual.click = False
                    self.chessVisual.creditsMenu()
