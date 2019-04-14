from tripleT.tictactoe import Game
from tripleT.dumbAI import DumbAI
from tripleT.smartAI import smartAI

opponent = DumbAI()
agent = smartAI(0.5, 0.01, 0.33, 0.99)
num_tgames = 5000
gamesplayed = 0

while (gamesplayed <= num_tgames):
    #number of training sessions
    game = Game(opponent = opponent, smartai = agent) 
    game.play()
    gamesplayed += 1
