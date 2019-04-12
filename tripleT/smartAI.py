import random
import pickle

class smartAI:

    def __init__(self, alpha, gamma, epsilon, eps_decay):
        self.alpha = alpha #learning rate
        self.gamma = gamma #discount rate
        self.epsilon = epsilon #exploration rate
        self.eps_decay = eps_decay #how quickly to slow down exploration rate; multiplied with the epsilon each round (should be 1 > x > 0)
        self.Qtable = {} #the Q-table

        self.prevBoard = None 
        self.lastStateAction = None
        self.lastQ = 0.0 

    def getQ(self, state, action):
        if (self.Qtable.get((state, action))) is None: #if there is no q-value for that 
            self.Qtable[(state, action)] = 1.0
        return self.Qtable.get((state, action))

    def updateQ(self, reward, state, possible_moves):
        q_list=[]
        for moves in possible_moves:
            q_list.append(self.getQ(tuple(state), moves))
        if q_list:
            max_q_next = max(q_list)
        else:
            max_q_next=0.0
        self.Q[self.state_action_last] = self.q_last + self.alpha * ((reward + self.gamma*max_q_next) - self.q_last)

    def getMove(self, board):
        self.prevBoard = ''.join(board) #convert the array into string so that it can be used as a key to the dict Qtable

        possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 9] 
        if random.random() < self.epsilon:
            #Explore
            move = possibleMoves[random.randint(0, len(possibleMoves) - 1)]
            self.epsilon *= self.eps_decay
            self.lastStateAction = (self.prevBoard, move)
            self.lastQ = self.getQ(self.prevBoard, move)
            return move #pick a random move from the possible moves
        else:
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
            #self.lastQ = self.getQ(self.prevBoard, possibleMoves)
            return possibleMoves[i_move]

    def saveQtable(self, file_name):
        with open(file_name, 'wb') as handle:
            pickle.dump(self.Qtable, handle, protocol = pickle.HIGHEST_PROTOCOL)

    def loadQtable(self, file_name):
        with open(file_name, 'rb') as handle:
            self.Qtable = pickle.load(handle)