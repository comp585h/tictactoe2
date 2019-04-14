from tripleT.tictactoe import Game
from tripleT.dumbAI import DumbAI
from tripleT.smartAI import smartAI

opponent = DumbAI()
agent = smartAI(0.3, 0.95, 0.2, 0.99)
num_tgames = 5000

t_games = 1000

#number of training sessions
game = Game(opponent = opponent, smartai = agent) 
game.play()
