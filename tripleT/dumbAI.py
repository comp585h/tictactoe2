from tripleT.tictactoe import Game
import random

class DumbAI:
# DumbAI taken from https://techwithtim.net/tutorials/python-programming/tic-tac-toe-tutorial/
# This 'dumb' AI follows this algorithm to make its move:
# 1. If there is a winning move take it
# 2. If the opponent has a possible winning move on their next turn, move into that position
# 3. Take any one of the corners. If more than one is available, randomly decide
# 4. Take the center position
# 5. Take one of the edges. If more than one is available, randomly decide
    def __init__(self, randomness):
        self.randomness = randomness

    def getMove(self, board):
        #obtain array of possible moves
        possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 9] 

        if random.random() < self.randomness:
            move = possibleMoves[random.randint(0, len(possibleMoves) - 1)]
            return move
        else:
            #check for possible winning move, or block opponent from possible winning move--thus, we don't need to take into account who is x and o, because regardless, we take the winning move
            for let in ['O', 'X']:
                for i in possibleMoves:
                    #make a copy of the current board state, and try out all the possible next moves; : 
                    boardCopy = board[:]
                    boardCopy[i] = let
                    checkgame = Game()
                    if checkgame.checkForWin(let, boardCopy):
                        return i

            #Try to take one of the corners
            cornersOpen = []
            for i in possibleMoves:
                if i in [0, 2, 6, 8]:
                    cornersOpen.append(i)
            if len(cornersOpen) > 0:
                move = selectRandom(cornersOpen)
                return move
            
            #Try to take the center
            if 4 in possibleMoves:
                move = 5
                return move

            #Take any edge
            edgesOpen = []
            for i in possibleMoves:
                for i in [1, 3, 5, 7]:
                    edgesOpen.append(i)
            
            if len(edgesOpen) > 0:
                move = selectRandom(edgesOpen)
            
            #shouldn't reach this, since above should be all possibilities
            return move

def selectRandom(li):
    ln = len(li)
    r = random.randrange(0, ln)
    return li[r]