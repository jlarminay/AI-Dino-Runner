import os
import time
from datetime import datetime

from functions.imageModifier import *
from functions.fileWriter import *
from functions.windowManager import *

## create driver and window
driver, window = createWindow()

## test screengrab
# screenshot = screenGrab(window, 'images/window.jpg')
# screenshot = cropImage(screenshot, 168, 290, 168+602, 290+143)
# saveImage(screenshot, 'images/area.jpg') 

## create log file
logname = 'processing/logs.txt'
newFile(logname)
writeToFile(logname, 'Game started')

## set intiial scores
bestGame = 0
bestScore = 0
games = 0
maxGames = 5

while(games < maxGames):

  ## restart game
  time.sleep(1.0)
  window.send_keys(Keys.SPACE)
  startTime = datetime.now()
  time.sleep(1.0)

  i = 0
  while(True):

    ## take image
    screenshot = screenGrab(window, 'processing/window.jpg')
    screenshot = cropImage(screenshot, 168, 290, 168+602, 290+143)
    resultImage = screenshot 
    
    ## check if game is over
    containGameOver = doesImageContain('data/gameover.jpg', screenshot)
    if(containGameOver):
      break

    ## check for object in from of dino
    jumparea = cropImage(screenshot, 68, 85, 68+120, 85+36)
    # saveImage(jumparea, 'processing/jumparea.jpg')
    colors = getColorsFromImage(jumparea)
    if(len(colors)>1):
      window.send_keys(Keys.SPACE)
    
    ## get all cactus positions biggest to smallest obstacle
    allObstacles = [
      ['data/cactus1.jpg', (0,0,255)], #red
      ['data/cactus2.jpg', (0,255,0)], #green
      ['data/cactus3.jpg', (255,0,0)], #blue
      ['data/cactus4.jpg', (255,0,128)] #purple
    ]
    foundObstacles = []
    for obs in allObstacles:
      foundObstacles += getPositionOfImage(obs[0], screenshot)
      resultImage = generateSearchImage(obs[0], resultImage, obs[1])
    ## save image for found obstacles
    # saveImage(resultImage, 'processing/results.jpg')

    ## print outs
    os.system('cls')
    print('games: '+str(games))
    print('i: '+str(i))
    print('len(colors): '+str(len(colors)))
    print('foundObstacles: '+str(len(foundObstacles)))
    print(foundObstacles)

    i += 1
  
  endTime = datetime.now()
  score = (endTime - startTime).total_seconds()
  writeToFile(logname, 'Game '+str(games)+' ended at: '+str(score))
  
  ## check if it beat PB
  if(score > bestScore):
    bestScore = score
    bestGame = games
    saveImage(screenshot, 'processing/bestscore.jpg')
  
  games += 1

writeToFile(logname, 'Game ended')
writeToFile(logname, 'Best game was '+str(bestGame)+' with a score of '+str(bestScore))
driver.close()
quit()
