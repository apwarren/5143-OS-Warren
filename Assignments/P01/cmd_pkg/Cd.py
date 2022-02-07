#Finished for now
import os

def cd(params = None):
  #User wants to go to home directory
  if(params is None or '~' in params[0]):
    os.chdir(os.path.expanduser('~'))

  #User wants to go to parent directory
  elif(params and '..' in params[0]):
    parent = os.getcwd()
    parent = parent.split('/')
    parent = parent[:-1]
    parent = '/'.join(parent)
    os.chdir(parent)

  elif params:
    if len(params) ==1:
      dirPath = params[0]
      if os.path.isdir(dirPath):    
        os.chdir(dirPath)
      elif os.path.isfile(dirPath):
        return('bash: cd: ' + dirPath + ': Not a directory')
      else:
        return('bash: cd: ' + dirPath + ': No such file or directory') 
    
    else:
      return('bash: cd: too many arguments')