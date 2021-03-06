import random
import pickle

class smartAI:

    def __init__(self, alpha, gamma, epsilon, eps_decay):
        self.alpha = alpha #learning rate
        self.gamma = gamma #discount rate
        self.epsilon = epsilon #exploration rate
        self.eps_decay = eps_decay #how quickly to slow down exploration rate; multiplied with the epsilon each round (should be 1 > x > 0)
        self.Qtable = {} #the Q-table; dictionary of (state, action) -> Q-value
        self.pastMoves= [] #a list of all past states

        self.prevBoard = None 
        self.lastStateAction = None
        self.lastQ = 0.0 

    def getQ(self, state, action):
        if (self.Qtable.get((state, action))) is None: #if there is no q-value for that 
            self.Qtable[(state, action)] = 1.0
            
        #print("gettingQ: {}".format(self.Qtable[(state,action)]))
        return self.Qtable.get((state, action))

    def updateQ(self, reward, state, board):
        #take care of adding the made move into list of past moves
        self.pastMoves.insert(0, self.lastStateAction)

        possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 9] 

        q_list=[]
        for moves in possibleMoves: #get q values for this new state of the board
            q_list.append(self.getQ(tuple(state), moves))
        if q_list:
            max_q_next = max(q_list) #max from list of q values of possible moves
            #print("max_q_next: {}".format(max_q_next))
        else:
            max_q_next=0.0
            #print("max_q_next: {}".format(max_q_next))
        
        #Updates the Q-value for all past moves
        for list_index in range(len(self.pastMoves)):
            self.Qtable[self.pastMoves[list_index]] += self.alpha * ((reward + (self.gamma**(list_index + 1)) * max_q_next) - self.Qtable[self.pastMoves[list_index]]) #updates Q's starting from most recent move to least recent move
        #print("update Q: {}".format(self.Qtable[self.lastStateAction]))

    def getMove(self, board):
        self.prevBoard = ''.join(board) #convert the array into string so that it can be used as a key to the dict Qtable

        possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 9] 
        if random.random() < self.epsilon:
            #print("exploring")
            #Explore
            move = possibleMoves[random.randint(0, len(possibleMoves) - 1)]
            self.epsilon *= self.eps_decay
            self.lastStateAction = (self.prevBoard, move)
            self.lastQ = self.getQ(self.prevBoard, move)
            #print("getMove stats: epsilon: {} lastStateAction: {} lastQ: {}".format(self.epsilon,self.lastStateAction, self.lastQ))
            return move #pick a random move from the possible moves
        else:
            #print("not exploring")
            Qlist = []

            #find the maximum Q-value for that board state and all the possible moves
            for action in possibleMoves:
                Qlist.append(self.getQ(self.prevBoard, action))
            maxQ = max(Qlist)

            if Qlist.count(maxQ) > 1:
                i_move = random.choice([i for i in range(len(possibleMoves)) if Qlist[i] == maxQ]) #creates list of the indexes where Qlist[i] = maxQ
            else: 
                i_move = Qlist.index(maxQ) #if only one of the max, just get the index of the maxQ

            self.epsilon *= self.eps_decay
            self.lastStateAction = (self.prevBoard, possibleMoves[i_move])
            self.lastQ = self.getQ(self.prevBoard, possibleMoves[i_move])
            #print("getMove stats: epsilon: {} lastStateAction: {} lastQ: {}".format(self.epsilon,self.lastStateAction, self.lastQ))
            return possibleMoves[i_move]

    def saveQtable(self, file_name):
        with open(file_name, 'ab') as handle:
            pickle.dump(self.Qtable, handle) #, protocol = pickle.HIGHEST_PROTOCOL

    def loadQtable(self, file_name):
        with open(file_name, 'rb') as handle:
            self.Qtable = pickle.load(handle)