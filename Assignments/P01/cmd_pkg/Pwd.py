import os

def pwd():
  """   
    NAME
        pwd - Print out what is the current working directory to the user
    SYNOPSIS
        pwd
    DESCRIPTION
        This command will get what directory the user is currently
        working out of and print out its path.
    USAGE
        pwd
          --Get the directory that the user is currently accessing and print it out
  """
  return os.getcwd()