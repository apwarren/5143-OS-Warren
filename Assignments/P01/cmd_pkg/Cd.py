#Finished for now
import os

def cd(params = None):
  """   
    NAME
        cd - change the current directory to a new given directory
    SYNOPSIS
        cd [OPTION] ... PATH
    DESCRIPTION
        This command will take the path given by the user and change
        the current working directory to be said path. If the path 
        does not exist then the command will print an error message to the user.
    USAGE
        cd ~
          --Go to the home directory of the system
        cd ..
          --Go to the parent directory of the current working directory
        cd DIRECTORY
          --Go to the directory of a given path
        cd PATH
          -- Go to a directory given its path
  """

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

  #User wants to go to a specific directory
  elif params:
    #Make sure only one path or directory is specified
    if len(params) == 1:
      #Get and change to new directory if it is an actual directory
      dirPath = params[0]
      if os.path.isdir(dirPath):    
        os.chdir(dirPath)
      
      #If the path leads to a file and not a directory then tell the user
      elif os.path.isfile(dirPath):
        print('cd: ' + dirPath + ': Not a directory')

      #If the path does not exist then tell the user as such
      else:
        print('cd: ' + dirPath + ': No such file or directory') 
    
    #More than one path or directory was given to the command
    else:
      print('cd: too many arguments')