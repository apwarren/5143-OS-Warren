#Finished for Now
import os

def cat(params):
  allFiles = ''
  for files in params:
    try:
      with open(files) as f:
        allFiles += f.read() + '\n'
      continue
    except Exception:
        if(files in os.listdir('.')):
          allFiles += "cat: " + files + ": Is a directory\n"
        else:
          allFiles += "cat: " + files + ": No such file or directory\n"
          
  return allFiles