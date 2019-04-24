import numpy as np
import Game
import time
import progressbar
import math
import tensorflow as tf


def record(rounds=1, filename=None):
    # AI's should store all of their own individual game data then,
    # at the end of recording I should be able to store their individual game data (X and O)
    ai_x = Game.Random_AI(Game.Tile.X)
    ai_o = Game.Random_AI(Game.Tile.O)
    # progress bar setup
    with progressbar.ProgressBar(max_value=rounds) as bar:
        # recording loop
        for i in range(0, rounds):
            my_game = Game.Game(ui=False, ai=True, ai_1=ai_x, ai_2=ai_o)
            (moves_left, winner) = my_game.run()
            #remove loser data
            if winner is Game.Tile.X:
                num_rows = int((9 - moves_left-1)/2)
                length = len(ai_o.state_data)
                for j in range(length-1, length-num_rows*9-1, -1):
                    ai_o.state_data.pop(j)
                    ai_o.move_data.pop(j)
            elif winner is Game.Tile.O:
                num_rows = int((9 - moves_left) / 2)
                length = len(ai_x.state_data)
                for j in range(length-1, length - num_rows * 9-1, -1):
                    ai_x.state_data.pop(j)
                    ai_x.move_data.pop(j)
            #TODO for testing, remove later
            bar.update(i)
    # reformat X datashape
    ai_x.state_data = np.array(ai_x.state_data)
    ai_x.state_data = ai_x.state_data.reshape((int(len(ai_x.state_data)/9)), 9)
    ai_x.move_data = np.array(ai_x.move_data)
    ai_x.move_data = ai_x.move_data.reshape((int(len(ai_x.move_data) / 9)), 9)
    # reformat O data shape
    ai_o.state_data = np.array(ai_o.state_data)
    ai_o.state_data = ai_o.state_data.reshape((int(len(ai_o.state_data) / 9)), 9)
    ai_o.move_data = np.array(ai_o.move_data)
    ai_o.move_data = ai_o.move_data.reshape((int(len(ai_o.move_data) / 9)), 9)
    # store data (for now we store O and O separately)
    if filename is None:
        x_name = input("X data name? \n")
        o_name = input("O data name? \n")
    else:
        (x_name, o_name) = filename
    np.save("Data/" + str(x_name), (ai_x.state_data, ai_x.move_data))
    np.save("Data/" + str(o_name), (ai_o.state_data, ai_o.move_data))


def get_data(o_file_path, x_file_path):
    o_state_data, o_move_data = np.load(o_file_path)
    x_state_data, x_move_data = np.load(x_file_path)
    state_data = np.vstack((o_state_data, x_state_data))
    move_data = np.vstack((o_move_data, x_move_data))

    # TODO potentially want to shuffle data

    return state_data, move_data


#assumes model with 9 dim input layer and 9 dim output (only for tic tac toe)
def train(o_file_path, x_file_path, model):
    (data, labels) = get_data(o_file_path, x_file_path)
    #TODO separate raw data into training validation and test
    data = tf.convert_to_tensor(data)
    labels = [np.where(r == 1)[0][0] for r in labels]
    labels = np.array(labels)
    labels = np.ndarray.flatten(labels)
    #print(labels.dtype)
    print("data shape: " + str(data))
    print("labels shape: " + str(labels))
    model.fit(data, labels, epochs=5, steps_per_epoch=100)
    #model_name = input("Model Name?: \n")
    model.save("Data/main_model_v2.h5")


def test(ai_x, ai_o, test_tile, rounds=1):
    with progressbar.ProgressBar(max_value=rounds) as bar:
        # recording loop
        wins = 0.0
        for i in range(0, rounds):
            my_game = Game.Game(ui=False, ai=True, ai_1=ai_x, ai_2=ai_o)
            (moves_left, winner) = my_game.run()
            if winner is test_tile:
                wins += 1
            bar.update(i)
    print()
    print(str(((wins/rounds)*100)) + "% win rate")


