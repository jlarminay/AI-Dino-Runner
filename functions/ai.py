import random

def shouldJump(
  time, 
  dinoPosition, 
  close1Distance, 
  close1Position, 
  close2Distance, 
  close2Position
):
  # ## check for object in from of dino
  # jumparea = cropImage(screenshot, 68, 85, 68+120, 85+36)
  # # saveImage(jumparea, processingFolder+'jumparea.jpg')
  # colors = getColorsFromImage(jumparea)
  # if(len(colors)>1):
  #   window.send_keys(Keys.SPACE)

  ## check distance to closest object
  if(close1Distance<150):
    hold_time = round(random.uniform(0.0, 0.5), 3)
    return True, hold_time
  
  return False, 0