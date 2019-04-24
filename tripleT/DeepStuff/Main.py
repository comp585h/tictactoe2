import AI
import tensorflow as tf
import Game
from tensorflow import keras

# for recording test data
#AI.record(1000000)

# setup a tf model
# model setup
'''
model = tf.keras.Sequential([
  tf.keras.layers.Dense(10, activation=tf.nn.relu, input_shape=(9,)),  # input shape required
  tf.keras.layers.Dense(10, activation=tf.nn.relu),
  tf.keras.layers.Dense(9)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
'''

my_model = tf.keras.models.load_model("Data/main_model_v2.h5")
'''
ai_o = Game.Random_AI(Game.Tile.O)
ai_x = Game.Smart_AI(model=my_model, tile_type=Game.Tile.X)
AI.test(ai_x, ai_o, test_tile=Game.Tile.X, rounds=1000)
'''
AI.train("Data/x1.npy", "Data/o1.npy", my_model)

#AI.get_data("Data/1milodata.npy", "Data/1milxdata.npy")