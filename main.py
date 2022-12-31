import os
import time
from datetime import datetime
from dotenv import load_dotenv

from functions.imageModifier import *
from functions.fileWriter import *
from functions.windowManager import *

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
    close1Distance = 10000
    close1Position = 0
    close2Distance = 10000
    close2Position = 0
    foundObstacles = []
    for obs in allObstacles:
      tmp = getPositionOfImage(obs[0], screenshot)
      if(len(tmp)>0):
        for ob in tmp:
          if(ob[0]-68 > 0):
            foundObstacles += [[ob, ob[0]-68]]
          # if((ob[0]-68 < closestObstacleDistance) and (ob[0]-68>0)):
          #   closestObstacleDistance = ob[0]-68
          #   closestObstaclePosition = ob[1]
        resultImage = generateSearchImage(obs[0], resultImage, obs[1])
    
    ## save image for found obstacles
    saveImage(resultImage, processingFolder+'obstacles.jpg')
    
    foundObstacles = sorted(foundObstacles, key=lambda l:l[1])
    
    # find closest object
    if(len(foundObstacles)>=1):
      close1Distance = foundObstacles[0][1]
      close1Position = foundObstacles[0][0][1]
    # find next closest
    if(len(foundObstacles)>=2):
      close2Distance = foundObstacles[1][1]
      close2Position = foundObstacles[1][0][1]
    
    # ## check for object in from of dino
    # jumparea = cropImage(screenshot, 68, 85, 68+120, 85+36)
    # # saveImage(jumparea, processingFolder+'jumparea.jpg')
    # colors = getColorsFromImage(jumparea)
    # if(len(colors)>1):
    #   window.send_keys(Keys.SPACE)

    ## check distance to closest object
    if(close1Distance<150):
      window.send_keys(Keys.SPACE)


    ## print outs
    os.system('cls')
    print('maxGames: '+str(maxGames))
    print('games: '+str(games))
    print('i: '+str(i))
    print('score: '+str((datetime.now() - startTime).total_seconds()))
    print('avg fps: '+str(i / (datetime.now() - startTime).total_seconds()))
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
