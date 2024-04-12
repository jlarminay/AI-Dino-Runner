import os
import tensorflow as tf
import numpy as np
import os
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from functions.imageModifier import *
from functions.fileWriter import *
from functions.windowManager import *
from functions.calculations import *
from functions.ai import *

processingFolder = str(os.getenv('PROCESSING_FOLDER'))
neuralFolder = str(os.getenv('NEURAL_NETWORK_FOLDER'))
maxGames = int(os.getenv('MAX_GAMES'))

numActions = 2
inputShape = (602, 151, 1)

# Create a neural network model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=inputShape),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(numActions)  # Linear activation for Q-values
])

# Constants for training
initial_exploration_rate = 0.1
final_exploration_rate = 0.01
exploration_rate_decay = (initial_exploration_rate - final_exploration_rate) / 500
discount_factor = 0.95

# Create the folders if they don't exist
create_folder_if_not_exists(processingFolder)
create_folder_if_not_exists(neuralFolder)

def preprocess_data(startTime, window):
    ## take image
    screenshot = screenGrab(window, processingFolder+'window.jpg')
    screenshot = cropImage(screenshot, 168, 281, 168+602, 281+151)

    # check if game over
    containGameOver = doesImageContain('data/gameover.jpg', screenshot)
    if(containGameOver):
      return False

    resultImage = screenshot

    ## get position of dino
    dinoPosition = getPositionOfImage('data/dino.jpg', screenshot)
    # dinoPosition = abs(dinoPosition[0][1] - 102)
    resultImage = generateSearchImage('data/dino.jpg', resultImage, (0,0,0))

    ## get position of obstacles
    allPossibleObstacles = [
      ['data/cactus1.jpg', (0,0,255)], #red
      ['data/cactus2.jpg', (0,255,0)], #green
      ['data/cactus3.jpg', (255,0,0)], #blue
      ['data/cactus4.jpg', (255,0,128)], #purple
      ['data/cactus5.jpg', (0,137,255)], #orange
      ['data/cactus6.jpg', (188,0,255)], #pink
      ['data/bird1.jpg', (0,77,89)], #pink
      ['data/bird2.jpg', (0,77,89)], #pink
    ]
    allObstacles = findObstacles(allPossibleObstacles, screenshot, resultImage)

    processed_data = {
        'dinoPos': dinoPosition,
        'obstacles': allObstacles,
        'score': (datetime.now() - startTime).total_seconds()
    }

    return processed_data

def choose_action(state, exploration_rate):
    # Exploration-exploitation trade-off
    if np.random.rand() < exploration_rate:
        return np.random.choice(numActions)
    else:
        # Choose the action with the highest Q-value predicted by the neural network
        q_values = model.predict(state)
        return np.argmax(q_values)

def update_model(state, action, reward, next_state, discount_factor):
    # Calculate the target Q-value
    target = reward + discount_factor * np.max(model.predict(next_state))

    # Get the current Q-values predicted by the model
    current_q_values = model.predict(state)

    # Update the Q-value of the chosen action
    current_q_values[0][action] = target

    # Train the model on the updated Q-values
    model.fit(state, current_q_values, epochs=1, verbose=0)

def train_dino_agent(attempts=1000, exploration_rate=initial_exploration_rate):
    # Initialization
    driver, window = createWindow()

    for episode in range(attempts):
        # Restart game
        time.sleep(1.0)
        window.send_keys(Keys.SPACE)
        startTime = datetime.now()
        time.sleep(1.0)

        total_reward = 0
        while not False:
            
            state = preprocess_data(startTime, window)
            
            # check if game over
            if not state:
                # game over
                update_model(state, action, reward, next_state, discount_factor)
                break

            action = choose_action(state, exploration_rate)

            # Print debug information
            os.system('cls')
            print(f"Episode {episode + 1}, Frame: {state['score']}, Action: {action}")

            # Simulate the chosen action in the game environment and get the next state and reward
            # next_state, reward, game_over = simulate_action(action)

            # Update the neural network model based on the observed reward
            update_model(state, action, reward, next_state, discount_factor)

            # Accumulate total reward
            # total_reward += reward

        print(f"Episode {episode + 1}, Total Reward: {total_reward}")

    # Save the updated model
    model.save(neuralFolder + 'dino_model.h5')

# Call the training function with additional episodes
train_dino_agent(attempts=100, exploration_rate=initial_exploration_rate)
