from tripleT.tictactoe_no_print import Game
from tripleT.dumbAI import DumbAI
from tripleT.smartAI_no_print import smartAI

randomness = 0.00

alpha = 0.7
gamma = 0.01
epsilon = 0.59
eps_decay = 0.999

opponent = DumbAI(randomness)
agent = smartAI(alpha, gamma, epsilon, eps_decay)

num_tgames = 1000000
gamesplayed = 0 

print("num of game = {}, randomness = {}, alpha = {}, gamma = {}, epsilon = {}, eps_decay = {}".format(num_tgames,randomness,alpha,gamma,epsilon,eps_decay))
agentW = 0
dumbW = 0
draw = 0

# agent.loadQtable("./qTable1.pickle")
while (gamesplayed <= num_tgames):
    #number of training sessions
    game = Game(opponent = opponent, smartai = agent) 
    game.play(training = True)
    gamesplayed += 1
    if game.winresult == 1:
        agentW += 1
    elif game.winresult == -1:
        dumbW += 1
    elif game.winresult == 0:
        draw += 1
# agent.saveQtable("./qTable1.pickle")

stats = "smart {} dumb {} draw {}, winrate = {}, dumb winrate = {}"
total = agentW + dumbW + draw
print(stats.format(agentW,dumbW,draw,agentW/total*100, dumbW/total*100))
