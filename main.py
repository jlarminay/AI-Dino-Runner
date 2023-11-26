import os
import time
from datetime import datetime
from dotenv import load_dotenv

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from functions.imageModifier import *
from functions.fileWriter import *
from functions.windowManager import *
from functions.calculations import *
from functions.ai import *

load_dotenv()

## set global variables
processingFolder = str(os.getenv('PROCESSING_FOLDER'))
maxGames = int(os.getenv('MAX_GAMES'))
bestGame = 0
bestScore = 0
games = 0
avgFPS = 0
avgScore = 0

## create driver and window
driver, window = createWindow()

## create log file
logname = processingFolder+'logs.txt'
newFile(logname)
writeToFile(logname, 'Game started')

while(games < maxGames):

  ## restart game
  time.sleep(1.0)
  window.send_keys(Keys.SPACE)
  startTime = datetime.now()
  time.sleep(1.0)

  i = 0
  while(True):

    ## take image
    screenshot = screenGrab(window, processingFolder+'window.jpg')
    screenshot = cropImage(screenshot, 168, 281, 168+602, 281+151)
    
    ## check if game is over
    containGameOver = doesImageContain('data/gameover.jpg', screenshot)
    if(containGameOver):
      break

    resultImage = screenshot 

    ## get position of dino
    dinoPosition = getPositionOfImage('data/dino.jpg', screenshot)
    dinoPosition = abs(dinoPosition[0][1] - 102)
    # resultImage = generateSearchImage('data/dino.jpg', resultImage, (0,0,0))
    
    ## get all cactus positions biggest to smallest obstacle
    allObstacles = [
      ['data/cactus1.jpg', (0,0,255)], #red
      ['data/cactus2.jpg', (0,255,0)], #green
      ['data/cactus3.jpg', (255,0,0)], #blue
      ['data/cactus4.jpg', (255,0,128)], #purple
      ['data/cactus5.jpg', (0,137,255)], #orange
      ['data/cactus6.jpg', (188,0,255)], #pink
      ['data/bird1.jpg', (0,77,89)], #pink
      ['data/bird2.jpg', (0,77,89)], #pink
    ]
    close1Distance, close1Position, close2Distance, close2Position = findObstacles(allObstacles, screenshot, resultImage)

    should_jump, hold_time = shouldJump(
      (datetime.now() - startTime).total_seconds(),
      dinoPosition,
      close1Distance,
      close1Position,
      close2Distance,
      close2Position
    )
    if(should_jump > 0):
      actions = ActionChains(driver)
      actions.key_down(Keys.SPACE)
      actions.pause(hold_time)
      actions.key_up(Keys.SPACE)
      actions.perform()

    ## print outs
    os.system('cls')
    print('maxGames: '+str(maxGames))
    print('games: '+str(games))
    print('i: '+str(i))
    print('score: '+str((datetime.now() - startTime).total_seconds()))
    print('avg fps: '+str(i / (datetime.now() - startTime).total_seconds()))
    print('')
    print('should_jump: '+str(should_jump))
    print('hold_time: '+str(hold_time))
    print('')
    # print('colors: '+str(len(colors)))
    # print('')
    # print('closestObstacleDistance: '+str(closestObstacleDistance))
    # print('closestObstaclePosition: '+str(closestObstaclePosition))
    print('')
    print('timeElapsed: '+str((datetime.now() - startTime).total_seconds()))
    print('dinoPosition: '+str(dinoPosition))
    print('close1Distance: '+str(close1Distance))
    print('close1Position: '+str(close1Position))
    print('close2Distance: '+str(close2Distance))
    print('close2Position: '+str(close2Position))

    i += 1
  
  endTime = datetime.now()
  score = (endTime - startTime).total_seconds()

  writeToFile(logname, 'Game '+str(games)+' with score '+str(score))
  
  avgFPS += i/score
  avgScore += score

  ## check if it beat PB
  if(score > bestScore):
    bestScore = score
    bestGame = games
    saveImage(screenshot, processingFolder+'bestscore.jpg')
  
  games += 1

writeToFile(logname, 'Game ended')
writeToFile(logname, 'Stats')
writeToFile(logname, ' - best game: '+str(bestGame))
writeToFile(logname, ' - best score: '+str(bestScore))
writeToFile(logname, ' - avg fps: '+str(avgFPS/maxGames))
writeToFile(logname, ' - avg score: '+str(avgScore/maxGames))
driver.close()
quit()
