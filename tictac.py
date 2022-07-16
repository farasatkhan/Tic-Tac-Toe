import pygame
import time

class TicTacToe:
    screen = None

    # Loading assets from folder
    X_IMG = pygame.image.load('assets/x_128.png')
    O_IMG = pygame.image.load('assets/o_128.png')
    BOARD_IMG = pygame.image.load('assets/board_600.png')

    # 1 represent 'X' and -1 represent 'O'
    currentPlayerMove = 1

    # You will start with an empty board – state should look like
    board = [[None, None, None], [None, None, None], [None, None, None]]

    # graphics store the image associated at the location and the location of the image of the screen
    graphics = [
            [[None, None], [None, None], [None, None]],
            [[None, None], [None, None], [None, None]],
            [[None, None], [None, None], [None, None]]
    ]

    # initalize the WIDTH and HEIGHT of the screen
    def __init__ (self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    # currentPos() is used for debugging purposes - it is shown on the top-left of the screen
    def currentPos(self):
        current_pos = pygame.mouse.get_pos()
        displayFont = pygame.font.Font('freesansbold.ttf', 18)
        displayText = displayFont.render("Current Pos: " + str(current_pos), True, (0, 0, 0))
        self.screen.blit(displayText, (10, 10))

    # render_board(board, ximg, oimg) - takes three arguments board, ximg and oimg
    # Explanation: The method is used to render the image on the screen 
    def render_board(self, board, ximg, oimg):
        for i in range(3):
            for j in range(3):
                if board[i][j] == 1:
                    self.graphics[i][j][0] = ximg
                    if i == 0:
                        self.graphics[i][j][1] = ximg.get_rect(center=(j*200+130, i*200+115))
                    else:
                        self.graphics[i][j][1] = ximg.get_rect(center=(j*200+130, i*200+130))

                elif board[i][j] == -1:
                    self.graphics[i][j][0] = oimg
                    if i == 0:
                        self.graphics[i][j][1] = oimg.get_rect(center=(j*200+130, i*200+115))
                    else:
                        self.graphics[i][j][1] = oimg.get_rect(center=(j*200+130, i*200+130))

    # move(board, player_move) - takes two arguments board and player_move
    # Explanation: This method is called when the user clicks on the one of the nine boxes and convert the pixels
    # into x and y position for the board. We divide the location of the mouse by 430 * 2 to get in the range 0-2
    # for xPos and yPos. Once the player played his move, then it is AI's move and the best location is picked using
    # alpha-beta pruning. bestAIMove store the best position for x and y and at the end we render the board.
    def move(self, board, player_move):
        position = pygame.mouse.get_pos()
        xPos = (position[0]) / 430 * 2
        yPos = (position[1]) / 430 * 2

        if board[int(yPos)][int(xPos)] is None:
            board[int(yPos)][int(xPos)] = player_move

            if player_move != 1: player_move = 1
            else: player_move = -1

            self.render_board(board, self.X_IMG, self.O_IMG)

            bestAIMove = self.alphaBetaPruning(board, len(self.emptySpaceList(board)), float("-inf"), float("inf"), player_move)
            self.AImove(board, player_move, bestAIMove[0], bestAIMove[1])

            if player_move != 1: player_move = 1
            else: player_move = -1

        self.render_board(board, self.X_IMG, self.O_IMG)

        return board, player_move

    # AImove(board, player_move, xPos, yPos) - takes 4 arguments
    # Explanation: This method is used to fill the board at the xPos and yPos coordinate
    def AImove(self, board, player_move, xPos, yPos):
        if board[xPos][yPos] is None:
            board[xPos][yPos] = player_move
        
        return board, player_move

    ### Alpha Beta Pruning Starts Here ###

    # AImoveNone(board, xPos, yPos) - takes 3 arguments
    # Explanation: This method is used to undo the action of the AImove. It is used in the alpha-beta pruning
    # function. We have to undo the actions in the alpha-beta pruning because we have a single 3x3 board.
    def AImoveNone(self, board, xPos, yPos):
        if board[xPos][yPos] is not None:
            board[xPos][yPos] = None
    
    # emptySpaceList(board) - takes 1 argument
    # Explanation: This method is used to return an array containing all the empty spots on the board available.
    # Returns: The function return an array containing empty spots on the board.
    def emptySpaceList(self, board):
        emptySpace = []
        for x, row in enumerate(board):
            for y, col in enumerate(row):
                if col is None:
                    emptySpace.append([x, y])
        return emptySpace

    # utlityValue()
    # Explanation: This function is used in the alpha-beta pruning to return 10 if 1 wins which in this case is
    # 'X' player and returns -10 if -1 wins which is 'O' player. We have associated 10 for the human player and
    # -10 for the AI Bot.
    # Returns: returns either 10, -10, or 0 in case of draw.
    def utlityValue(self):
        if self.win_status_unrendered(self.board) == 1:
            return 10
        elif self.win_status_unrendered(self.board) == -1:
            return -10
        else:
            return 0

    # alphaBetaPruning(board, depth, alpha, beta, player) - takes 5 arguments
    # Explanation: This method is used to return the best possible moves for the AI. We contiously call the function
    # till the depth is reached to 0 or either 1 wins which is 'X' or -1 which in this case is 'O'. We recursively call
    # the function reducing the depth which is the length of the empty spots available on the 3x3 board. We call and
    # AImove function to place the item on the board and undo the action using the AImoveNone.
    # Returns: The function returns the best row, best column and the utility value associated with it in
    # an array of size 3. 
    def alphaBetaPruning(self, board, depth, alpha, beta, player):
        row = -1
        col = -1

        if depth == 0 or (self.win_status_unrendered(board) != 0 and self.win_status_unrendered(board) is not None):
            return [row, col, self.utlityValue()]
        else:
            for cell in self.emptySpaceList(board):
                self.AImove(board, player, cell[0], cell[1])
                score = self.alphaBetaPruning(board, depth - 1, alpha, beta, -player)
                if player == 1:
                    if score[2] > alpha:
                        alpha = score[2]
                        row = cell[0]
                        col = cell[1]
                else:
                    if score[2] < beta:
                        beta = score[2]
                        row = cell[0]
                        col = cell[1]
                self.AImoveNone(board, cell[0], cell[1])

                if alpha >= beta:
                    break

            if player == 1:
                return [row, col, alpha]
            else:
                return [row, col, beta]

    # END OF ALPHA BETA PRUNING

    # win_status_unrendered(board): takes 1 argument
    # Explanation: This method is used to check for the winning status of the game. This method is similar to
    # win_status in the sense that both functions checks the winning status. The only difference is that this function
    # does not then render it on the screen.
    # Returns: 1 if 'X' wins, -1 if 'O' wins and 0 if game is draw. 
    def win_status_unrendered(self, board):
        winner = None

        for row in range(3):
            if board[row][0] is not None and board[row][0] == board[row][1] and board[row][1] == board[row][2]:
                return board[row][0]
        for col in range(3):
            if board[0][col] is not None and board[0][col] == board[1][col] and board[1][col] == board[2][col]:
                return board[0][col]
        if board[0][0] is not None and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            return board[0][0]
        if board[0][2] is not None and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            return board[0][2]

        if winner is None:
            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] != 1 and board[i][j] != -1:
                        return None
            return 0

    # win_status_unrendered(board): takes 1 argument
    # Explanation: This method is used to check for the winning status of the game. This method is same as above but
    # only difference is that this method then render the winning board on the screen.
    # Returns: 1 if 'X' wins, -1 if 'O' wins and 0 if game is draw. 
    def win_status(self, board):
        winner = None

        # Check Rows for winning
        for row in range(3):
            if board[row][0] is not None and board[row][0] == board[row][1] and board[row][1] == board[row][2]:
                winner = board[row][0]
                winner_translate = "X" if winner == 1 else "O"

                for i in range(3):
                    self.graphics[row][i][0] = pygame.image.load(f'assets/{winner_translate}_128_green.png')
                    self.screen.blit(self.graphics[row][i][0], self.graphics[row][i][1])
                pygame.display.update()
                return winner
        
        # Check Columns for winning
        for col in range(3):
            if board[0][col] is not None and board[0][col] == board[1][col] and board[1][col] == board[2][col]:
                winner = board[0][col]
                winner_translate = "X" if winner == 1 else "O"
                for i in range(3):
                    self.graphics[i][col][0] = pygame.image.load(f'assets/{winner_translate}_128_green.png')
                    self.screen.blit(self.graphics[i][col][0], self.graphics[i][col][1])
                pygame.display.update()
                return winner

        # Check Diagnols for winning
        if board[0][0] is not None and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            winner = board[0][0]
            winner_translate = "X" if winner == 1 else "O"
            for i in range(3):
                self.graphics[i][i][0] = pygame.image.load(f'assets/{winner_translate}_128_green.png')
                self.screen.blit(self.graphics[i][i][0], self.graphics[i][i][1])
            pygame.display.update()
            return winner

        if board[0][2] is not None and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            winner = board[0][2]
            winner_translate = "X" if winner == 1 else "O"
            for i in range(3):
                self.graphics[i][2-i][0] = pygame.image.load(f'assets/{winner_translate}_128_green.png')
                self.screen.blit(self.graphics[i][2-i][0], self.graphics[i][2-i][1])
            pygame.display.update()
            return winner

        # Check if there is still empty spots available on the board.
        if winner is None:
            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] != 1 and board[i][j] != -1:
                        return None
            return 0

    def run(self):
        # Initializing and loading the assets to display
        pygame.init()
        pygame.display.set_caption("Tic Tac Toe")
        icon = pygame.image.load('assets/icon.png')
        pygame.display.set_icon(icon)

        gameEnded = False
        running = True
        checkGameStatus = False
        while running:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.BOARD_IMG, (25, 25))
            self.currentPos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # When MOUSEBUTTONDOWN is pressed we call the move function to take the x and y coordinates of the screen
            # and converts it in the range 0-2 and insert at the appropriate position in the 3x3 board.
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.board, self.currentPlayerMove = self.move(self.board, self.currentPlayerMove)
                checkGameStatus = True

            # Display the images on the screen
            for i in range(3):
                for j in range(3):
                    if self.graphics[i][j][0] is not None:
                        self.screen.blit(self.graphics[i][j][0], self.graphics[i][j][1])

            if checkGameStatus:
                if self.win_status(self.board) is not None:
                    gameEnded = True
                    pygame.display.update()
                    time.sleep(1)

                # When the game is ended then we create a new board and new graphic for the images assets and 
                # the coordinates of the assets on the screen.
                if gameEnded:
                    self.currentPlayerMove = 1

                    self.board = [[None, None, None], [None, None, None], [None, None, None]]
                    self.graphics = [
                            [[None, None], [None, None], [None, None]],
                            [[None, None], [None, None], [None, None]],
                            [[None, None], [None, None], [None, None]]
                    ]

                    gameEnded = False

                checkGameStatus = False

            pygame.display.update()