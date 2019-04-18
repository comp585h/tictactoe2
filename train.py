from tripleT.tictactoe_no_print import Game
from tripleT.dumbAI import DumbAI
from tripleT.smartAI_no_print import smartAI


opponent = DumbAI(0.00)
agent = smartAI(0.5, 0.01, 0.5, 0.9999)

num_tgames = 100000
gamesplayed = 0 

agentW = 0
dumbW = 0
draw = 0

agent.loadQtable("./qTable.pickle")
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
agent.saveQtable("./qTable.pickle")

stats = "smart {} dumb {} draw {}, winrate = {}, dumb winrate = {}"
total = agentW + dumbW + draw
print(stats.format(agentW,dumbW,draw,agentW/total*100, dumbW/total*100))
