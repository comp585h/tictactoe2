from tripleT.tictactoe import Game
from tripleT.dumbAI import DumbAI
from tripleT.smartAI import smartAI
from tripleT.DeepStuff import Game as gm
import tensorflow as tf
import progressbar

my_model = tf.keras.models.load_model("tripleT/Data/main_model_v2.h5")



better_ai = gm.Smart_AI(model=my_model, competition=True)

opponent = DumbAI(0.00)
agent = smartAI(0.5, 0.01, 0.5, 0.9999)

num_tgames = 1000
gamesplayed = 0 

agentW = 0
dumbW = 0
draw = 0

agent.loadQtable("./qTable.pickle")
with progressbar.ProgressBar(max_value=num_tgames) as bar:
    i = 0
    while (gamesplayed <= num_tgames):
        # number of training sessions
        game = Game(opponent=better_ai, smartai=agent)
        game.play(training=True)
        gamesplayed += 1
        if game.winresult == 1:
            agentW += 1
        elif game.winresult == -1:
            dumbW += 1
        elif game.winresult == 0:
            draw += 1
        bar.update(i)
        i+=1
agent.saveQtable("./qTable.pickle")

stats = "smart {} dumb {} draw {}, winrate = {}, dumb winrate = {}"
total = agentW + dumbW + draw
print(stats.format(agentW,dumbW,draw,agentW/total*100, dumbW/total*100))

#agentW = 0
#dumbW = 0#
#draw = 0

#with open("./stats.txt",'r') as reading:
#    for i in reading:
#        agentW += int(i.split(" ")[0])
#        dumbW += int(i.split(" ")[1])
#       draw += int(i.split(" ")[2])
#total = agentW+dumbW+draw
#print(stats.format(agentW,dumbW,draw,agentW/total*100, dumbW/total*100))