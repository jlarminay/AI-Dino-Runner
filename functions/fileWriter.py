import os
from datetime import datetime

def newFile(filename):
  exploded = filename.split('/')[:-1]
  path = '/'.join(exploded)
  
  if(not os.path.exists(path)):
    os.makedirs(path)
  
  open(filename, 'w+').close()
  return

def writeToFile(filename, string):
  f = open(filename, 'a')
  n = datetime.now()
  f.write(n.strftime("[%Y-%m-%d %H:%M:%S:%f]"))
  f.write('\t')
  f.write(string)
  f.write('\n')
  f.close()
  return

def create_folder_if_not_exists(folder_path):
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def create_file_if_not_exists(file_path):
  if not os.path.exists(file_path):
    open(file_path, 'w').close()