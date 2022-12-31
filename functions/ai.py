
# Returns if the dino should jump
# 
# Possibles returns:
#  - 0 - dino should do nothing
#  - 1 - dino should jump
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
    return 1
  
  return 0