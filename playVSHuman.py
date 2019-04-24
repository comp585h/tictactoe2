from tripleT.tictactoe_no_print import Game
from tripleT.dumbAI import DumbAI
from tripleT.smartAI_no_print import smartAI
from tripleT.humanPlayer import Human


alpha = 0.7
gamma = 0.01
epsilon = 0.59
eps_decay = 0.999

opponent = Human()
agent = smartAI(alpha, gamma, epsilon, eps_decay)
print("alpha = {}, gamma = {}, epsilon = {}, eps_decay = {}".format(alpha,gamma,epsilon,eps_decay))

agent.loadQtable("./qTable1.pickle")
end = False
while (not end):
    #number of training sessions
    game = Game(opponent = opponent, smartai = agent) 
    game.play(training=False)
# agent.saveQtable("./qTable.pickle")
# stats = "smart {} dumb {} draw {}, winrate = {}, dumb winrate = {}"
# agentW = 0
# dumbW = 0
# draw = 0

# with open("./stats.txt",'r') as reading:
#     for i in reading:
#         agentW += int(i.split(" ")[0])
#         dumbW += int(i.split(" ")[1])
#         draw += int(i.split(" ")[2])
# total = agentW+dumbW+draw
# print(stats.format(agentW,dumbW,draw,agentW/total*100, dumbW/total*100))