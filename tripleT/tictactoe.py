import random

#Tic Tac Toe Game
class Game:
    def __init__(self, opponent=None, smartai=None):
        #you can plug in another opponent AI class--all that is required is that it has a getMove() method
        self.opponent = opponent
        self.smartai = smartai

        #game board is a simple array of positions 0 to 8, where the n-th number in array matches to the positions on the tic tac toe board like:
        # 0 | 1 | 2
        # ----------
        # 3 | 4 | 5
        # ----------
        # 6 | 7 | 8
        self.board = [' ' for x in range(9)]

    def makeMove(letter, pos):
        board[pos] = letter

    def checkForWin(self, letter, board):
        #has board as additional input as we call this in the opponent AI class--have to pass along board information
        #First check for diagonals
        a = [board[0], board[4], board[8]]
        b = [board[2], board[4], board[6]]

        #Use count method to see if letter is present 3 times
        if a.count(letter) == 3 or b.count(letter) == 3:
            return True

        #Then check for row/column win possibilities
        for i in range(3):
            col = [board[0 + i], board[3 + i], board[6 + i]]
            row = [board[i*3], board[i*3 + 1], board[i*3 + 2]]
            if col.count(letter) == 3 or row.count(letter) == 3:
                return True
        return False

    def checkForDraw(self):
        #Returns true if there no element missing in the board
        for pos in self.board:
            if pos == " ":
                return False
        return True

    def checkForEnd(self, letter, training):
        #Returns -1 if still continuing, 0 if draw, and 1 if a player has won
        #Check first if victorious, then draw
        if self.checkForWin(letter, self.board):
            if not training:
                printBoard(self.board)
            if letter == 'X':
                if not training:
                    print("Player 1 wins!")
            else:
                if not training:
                    print("Opponent wins!")
            return 1
        if self.checkForDraw():
            if not training:
                printBoard(self.board)
                print("It's a draw!")
            return 0
        return -1

    def play(self, training=True):
        #'Rolling of the dice' to decide who goes first
        if random.random() < 0.5:
            while True:
                #player goes first
                if not training:
                    printBoard(self.board)
                    print("Player's move:")
                move = self.smartai.getMove(self.board) #get the move from smartai
                self.board[move] = 'X'
                check = self.checkForEnd('X', training)
                if not check == -1:
                    reward = 1
                    break
                else:
                    reward = 0

                #then opponent
                if not training:
                    printBoard(self.board)
                    print("Opponent's move:")
                opponentAction = self.opponent.getMove(self.board)
                self.board[opponentAction] = 'O'

                check = self.checkForEnd('O', training)
                if not check == -1:
                    reward = -1
                    break
        else:
            while True:
                #opponent goes first
                if not training:
                    printBoard(self.board)
                    print("Opponent's move:")
                opponentAction = self.opponent.getMove(self.board)
                self.board[opponentAction] = 'X'

                check = self.checkForEnd('X', training)
                if not check == -1:
                    #opponent has won
                    reward = -1
                    break
                else:
                    #draw scenario
                    reward = 0

                #then player
                if not training:
                    printBoard(self.board)
                    print("Player's move:")
                move = self.smartai.getMove(self.board)
                self.board[move] = 'O'

                #check if game has ended
                check = self.checkForEnd('O', training)
                if not check == -1:
                    reward = 1
                    break

def printBoard(board):
    print('   |   |')
    print(' ' + board[0] + ' | ' + board[1] + ' | ' + board[2])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[3] + ' | ' + board[4] + ' | ' + board[5])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[6] + ' | ' + board[7] + ' | ' + board[8])
    print('   |   |')
