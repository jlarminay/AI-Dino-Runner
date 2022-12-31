import time
import pygetwindow
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import cv2

def createWindow():
  driver = webdriver.Edge()
  driver.set_script_timeout(10)
  driver.get("https://trex-runner.com")
  driver.set_window_size(1000, 600)

  # set window to overflow hidden to stop flickering
  driver.execute_script("document.getElementsByTagName('body')[0].style.overflow = 'hidden'")

  # click mute button
  driver.find_element(By.ID, 'mutebtn').click()

  element = driver.find_element(By.TAG_NAME, 'body')

  return driver, element

def screenGrab(window, filename):
  window.screenshot(filename)
  return cv2.imread(filename)