from tripleT.tictactoe_no_print import Game
from tripleT.dumbAI import DumbAI
from tripleT.smartAI_no_print import smartAI

opponent = DumbAI()
agent = smartAI(0.5, 0.01, 0.33, 0.99)
num_tgames = 100000
gamesplayed = 0
agent.loadQtable("./qTable.pickle")
while (gamesplayed <= num_tgames):
    #number of training sessions
    game = Game(opponent = opponent, smartai = agent) 
    game.play()
    gamesplayed += 1
agent.saveQtable("./qTable.pickle")
stats = "smart {} dumb {} draw {}, winrate = {}, dumb winrate = {}"
agentW = 0
dumbW = 0
draw = 0

with open("./stats.txt",'r') as reading:
    for i in reading:
        agentW += int(i.split(" ")[0])
        dumbW += int(i.split(" ")[1])
        draw += int(i.split(" ")[2])
total = agentW+dumbW+draw
print(stats.format(agentW,dumbW,draw,agentW/total*100, dumbW/total*100))