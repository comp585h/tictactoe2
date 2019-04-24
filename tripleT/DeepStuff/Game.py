'''
Base tic tac toe game
currently only implements human vs human play
need to consider how to properly implement AI for easy mutability
(i want to be able to just give the game AI inputs... do I have to pass in an AI?
probably. I'll just make 2 AI classes. the smart and dumb AI, and move them back in
pass in a smart AI and a dumb AI, currently no plans for a second smart AI, but
that shouldn't be too hard to add."

'''

import random
from enum import Enum
import numpy as np



#set up tile types
class Tile(Enum):
    X = 1
    O = -1
    E = 0

class Player:
    def __init__(self, tile_type=Tile.X):
        self.tile_type = tile_type

    #player can select an open space [0:8]
    def move(self, board):
        while True:
            space = int(input("Chose open tile: \n"))
            # for some reason we have to cast space as an int
            if space in board.open_tiles:
                return space
            else:
                # we assume players always play with UI so we allow prints
                print("Invalid Move")
                print(space)
                print(board.open_tiles)

def convert2state(my_array):
    state = []
    for tile in my_array:
        if tile == "X":
            state.append(Tile.X)
        elif tile == "O":
            state.append(Tile.O)
        elif tile == " ":
            state.append(Tile.E)
    #print(state)
    return state

# takes in an AI model
class Smart_AI:
    def __init__(self, model, tile_type=Tile.O, competition=False):
        self.competition = competition
        self.model = model
        self.tile_type = tile_type
        self.state_data = []
        self.move_data = []
        self.num_random_choices = 0
    def getMove(self, board):
        if self.competition:
            board = Board(convert2state(board))

        # need raw values of tiles instead of enum objects
        temp_state = []
        for i in board.state:
            self.state_data.append(i.value)
            temp_state.append(i.value)
        #print(np.array(board.state).shape)
        temp_state = np.array(temp_state)
        #print(temp_state.shape)

        choice = self.model.predict(temp_state.reshape(1, 9))
        choice = np.array(choice)
        choice = np.argmax(choice)
        #print(choice)
        # make sure AI choice is valid
        if choice not in board.open_tiles:
            choice = random.choice(board.open_tiles)
            self.num_random_choices += 1
        # create one hot array from choice and then append to move list
        one_hot = np.zeros(9).tolist()
        one_hot[choice] = 1
        # must append as individual elements and not lists
        for i in one_hot:
            self.move_data.append(i)
        return choice

class Random_AI:
    def __init__(self, tile_type=Tile.X):
        self.tile_type = tile_type
        self.state_data = []
        self.move_data = []

    def move(self, board):
        # need raw values of tiles instead of enum objects
        for i in board.state:
            self.state_data.append(i.value)
        choice = random.choice(board.open_tiles)
        # create one hot array from choice and then append to move list
        one_hot = np.zeros(9).tolist()
        one_hot[choice] = 1
        # must append as individual elements and not lists
        for i in one_hot:
            self.move_data.append(i)
        return choice

class MiniMax_AI:
    def __init__(self, tile_type=Tile.X):
        self.tile_type = tile_type
        self.state_data = []
        self.move_data = []

    def move(self, board):
        # need raw values of tiles instead of enum objects
        for i in board.state:
            self.state_data.append(i.value)
        choice = random.choice(board.open_tiles)
        # create one hot array from choice and then append to move list
        one_hot = np.zeros(9).tolist()
        one_hot[choice] = 1
        # must append as individual elements and not lists
        for i in one_hot:
            self.move_data.append(i)
        return choice



#TODO Realizing alot of this could be made less gross by using 2d numpy arrays but
#screew it i'll make a more efficient version later
# takes 9 tile types
class Board:
    def __init__(self, state):
        self.state = state
        #TODO this is kinda gross
        r1 = state[0].value + state[1].value + state[2].value
        r2 = state[3].value + state[4].value + state[5].value
        r3 = state[6].value + state[7].value + state[8].value
        c1 = state[0].value + state[3].value + state[6].value
        c2 = state[1].value + state[4].value + state[7].value
        c3 = state[2].value + state[5].value + state[8].value
        dlr = state[0].value + state[4].value + state[8].value
        drl = state[2].value + state[4].value + state[6].value
        self.win_states = [r1, r2, r3, c1, c2, c3, dlr, drl]
        open_tiles = []
        for i in range(0, 9):
            if state[i] is Tile.E:
                list.append(open_tiles, i)
        self.open_tiles = open_tiles


    def update(self, pos, tile_type):
        self.state[pos] = tile_type
        self.__init__(self.state)


    # X always plays first
    # in HH mode player_1 is X and player_2 is O
    # ui = True implies at least 1 human player
    # assumes that if second ai isn't put in as param that it is ai vs. human
class Game:
    def __init__(self, ai=False, ai_1=None, ai_2=None, ui=False):
        # I know ai should be lower case by convention but fuck conformity I like the upper case
        self.player_1 = Player(Tile.X)
        self.player_2 = Player(Tile.O)
        self.ai = ai
        self.ai_1 = ai_1
        self.ai_2 = ai_2
        initial_state = [Tile.E, Tile.E, Tile.E,
                         Tile.E, Tile.E, Tile.E,
                         Tile.E, Tile.E, Tile.E]
        self.board = Board(initial_state)
        self.ui = ui
        #is true if player 1's turn is false if player 2's turn
        self.turn = True
        self.end_game = False
        self.winner = None

    def game_logic(self):
        if self.game_over() is None:
            if not self.ai:
                if self.turn:
                    self.turn = False
                    if self.ui:
                        print(str(self.player_1.tile_type.name) + "'s move.")
                    move = self.player_1.move(self.board)
                    self.board.update(move, self.player_1.tile_type)
                else:
                    self.turn = True
                    if self.ui:
                        print(str(self.player_2.tile_type.name) + "'s move.")
                    move = self.player_2.move(self.board)
                    self.board.update(move, self.player_2.tile_type)
            else:
                if self.ai_2 is None:
                    # AI vs Human
                    if self.ai_1.tile_type is Tile.X:
                        if self.turn:
                            self.turn = False
                            if self.ui:
                                print(str(self.ai_1.tile_type.name) + "'s move.")
                            move = self.ai_1.move(self.board)
                            self.board.update(move, self.ai_1.tile_type)
                        else:
                            self.turn = True
                            if self.ui:
                                print(str(self.player_2.tile_type.name) + "'s move.")
                            move = self.player_2.move(self.board)
                            self.board.update(move, self.player_2.tile_type)
                    else:
                        if self.turn:
                            self.turn = False
                            if self.ui:
                                print(str(self.player_1.tile_type.name) + "'s move.")
                            move = self.player_1.move(self.board)
                            self.board.update(move, self.player_1.tile_type)
                        else:
                            self.turn = True
                            if self.ui:
                                print(str(self.ai_1.tile_type.name) + "'s move.")
                            move = self.ai_1.move(self.board)
                            self.board.update(move, self.ai_1.tile_type)

                else:
                    # AI vs AI implementation
                    if self.ai_1.tile_type is Tile.X:
                        if self.turn:
                            self.turn = False
                            if self.ui:
                                print(str(self.ai_1.tile_type.name) + "'s move.")
                            move = self.ai_1.move(self.board)
                            self.board.update(move, self.ai_1.tile_type)
                        else:
                            self.turn = True
                            if self.ui:
                                print(str(self.ai_2.tile_type.name) + "'s move.")
                            move = self.ai_2.move(self.board)
                            self.board.update(move, self.ai_2.tile_type)
                    else:
                        if self.turn:
                            self.turn = False
                            if self.ui:
                                print(str(self.ai_2.tile_type.name) + "'s move.")
                            move = self.ai_2.move(self.board)
                            self.board.update(move, self.ai_2.tile_type)
                        else:
                            self.turn = True
                            if self.ui:
                                print(str(self.ai_1.tile_type.name) + "'s move.")
                            move = self.ai_1.move(self.board)
                            self.board.update(move, self.ai_1.tile_type)

        else:
            self.winner = self.game_over()

    def game_over(self):
        if 3 in self.board.win_states:
            self.end_game = True
            return Tile.X
        elif -3 in self.board.win_states:
            self.end_game = True
            return Tile.O
        elif len(self.board.open_tiles) == 0:
            self.end_game = True
            return Tile.E
        else:
            return None


    def run(self):
        while not self.end_game:
            if self.ui:
                self.print_board()
            self.game_logic()
        if self.ui:
            print("++++++++++++++++++++++++++++++++++++")
            self.print_board()
            if(self.winner is not Tile.E):
                print(str(self.winner.name) + " Won!")
            else:
                print("Draw!")
        return len(self.board.open_tiles), self.winner



    def print_board(self):
        for i in range(0,3):
            print(str(self.board.state[i*3].name) + " "
                  + str(self.board.state[1 + i*3].name) + " "
                  + str(self.board.state[2 + i*3].name), end = " ||| ")
            print(str(i * 3) + " "
                  + str(1 + i * 3) + " "
                  + str(2 + i * 3))

