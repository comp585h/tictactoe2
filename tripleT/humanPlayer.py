from tripleT.tictactoe import Game

class Human:



    def getMove(self, board):
        possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 9]

        move = input('Enter move: Possible moves include {}: '.format(possibleMoves))
        while move not in ['0','1','2','3','4','5','6','7','8'] or int(move) not in possibleMoves:
            move = input("Invalid move. Possible moves include {}: ".format(possibleMoves))

        return int(move)
