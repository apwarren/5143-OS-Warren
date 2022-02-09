#Finished!!! It's fun when it doesn't take long
import os

def cp(params):
  originalPath = os.getcwd()
  #Error checking
  if(len(params) == 0):
    return('mv: missing file operand')

  if(len(params) == 1):
    return('mv: missing destination file operand after \'' + params[0] + '\'')

  if(len(params) > 2):
    return('mv: too many arguments')

  original = params[0]
  newFile = params[1]

  try:
    #We plan to move to another directory
    if('/' in original):
      originPath = original.split('/')
      original = originPath[-1]
      originPath = originPath[:-1]
      originPath = '/'.join(originPath)
      os.chdir(originPath)
    #Check to make sure a file is being copied
    with open(original) as f:
      info = f.read()

    #Go back to orignal directory
    os.chdir(originalPath)

    #We plan to move to another directory to put copy in
    if('/' in newFile):
      newPath = newFile.split('/')
      newFile = newPath[-1]
      newPath = newPath[:-1]
      newPath = '/'.join(newPath)
      os.chdir(newPath)

    #moving to a directory not another file
    if(os.path.isdir(newFile)):
      os.chdir(newFile)
      newFile = original
      
    #Copy contents into new file
    with open(newFile, 'w') as f:
      f.write(info)

    #Go back to orignal directory
    os.chdir(originalPath)
    
  except Exception:
    if(os.path.exists(original)):
      return ('mv: cannot stat \'' + newFile + '\': No such file or directory')
    else:
       return ('mv: cannot stat \'' + original + '\': No such file or directory')