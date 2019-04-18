from tripleT.tictactoe import Game
from tripleT.dumbAI import DumbAI
from tripleT.smartAI import smartAI
from tripleT.humanPlayer import Human

opponent = Human()
agent = smartAI(0.5, 0.01, 0.0, 0.99)
num_tgames = 5000
gamesplayed = 0
agent.loadQtable("./qTable.pickle")
end = False
while (not end):
    #number of training sessions
    game = Game(opponent = opponent, smartai = agent) 
    game.play(training=False)
    gamesplayed += 1
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