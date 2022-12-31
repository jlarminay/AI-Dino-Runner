import cv2
import numpy
from PIL import Image, ImageGrab

ImageSearchThreshold = 0.90

# def screenGrab(topleft,topright,bottomleft,bottomright):
#   screen = ImageGrab.grab(bbox=(
#     topleft,
#     topright,
#     bottomleft,
#     bottomright
#   ))
#   return convertImageToCV2(screen)

def convertImageToPIL(image):
  if(image.__class__.__name__=='Image'):
    return image
  return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def convertImageToCV2(image):
  if(image.__class__.__name__=='ndarray'):
    return image
  return cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)

def cropImage(original, top, left, width, height):
  newImage = convertImageToPIL(original)
  newImage = newImage.crop((top, left, width, height))
  return convertImageToCV2(newImage)

def doesImageContain(needle, haystack):
  cleanedNeedle = convertImageToCV2(loadImage(needle))
  cleanedHaystack = convertImageToCV2(loadImage(haystack))

  res = cv2.matchTemplate(cleanedHaystack, cleanedNeedle, cv2.TM_CCOEFF_NORMED)
  loc = numpy.where( res >= ImageSearchThreshold)
  return len(loc[0]) >= 1

def getPositionOfImage(needle, haystack):
  cleanedNeedle = convertImageToCV2(loadImage(needle))
  cleanedHaystack = convertImageToCV2(loadImage(haystack))
  h, w, c = cleanedNeedle.shape
  
  res = cv2.matchTemplate(cleanedHaystack, cleanedNeedle, cv2.TM_CCOEFF_NORMED)
  loc = numpy.where( res >= ImageSearchThreshold)
  
  results = []
  for pt in zip(*loc[::-1]):
    results.append(pt)
  # return results, h
  return results

def generateSearchImage(needle, haystack, color):
  cleanedNeedle = convertImageToCV2(loadImage(needle))
  cleanedHaystack = convertImageToCV2(loadImage(haystack))
  h, w, c = cleanedNeedle.shape
  
  res = cv2.matchTemplate(cleanedHaystack, cleanedNeedle, cv2.TM_CCOEFF_NORMED)
  loc = numpy.where( res >= ImageSearchThreshold)
  for pt in zip(*loc[::-1]):
    cv2.rectangle(cleanedHaystack, pt, (pt[0] + w, pt[1] + h), color, 2)
  
  return cleanedHaystack

def getColorsFromImage(image):
  image = convertImageToPIL(image)
  colors = image.convert('RGB').getcolors()
  return colors

def loadImage(filename):
  if(type(filename)==str):
    return cv2.imread(filename)
  return filename

def saveImage(image, filename):
  cv2.imwrite(filename, image)