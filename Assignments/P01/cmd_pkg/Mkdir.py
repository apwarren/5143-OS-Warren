import os

def mkdir(params):
  """   
    NAME
        mkdir - Make a new directory given a name
    SYNOPSIS
        mkdir NAME
    DESCRIPTION
        This command takes a given name and creates a new directory within
        the current working directory that is called by the given name.
        The new directory is empty at the beginning of its creation.
        Multiple directories can be make with one command. No flags
        are passed to this command.
    USAGE
        mkdir NAME
          --Make a directory and call it NAME
        mkdir NAME1 ... NAMEX
          --Make multiple directories and call them NAME1 ... NAMEX
  """

  #Traverse and create directories for as many names have been passed
  for newDirect in params:
    try:
      os.mkdir(newDirect)

    #Cannot create the directory because one of the same name already exists
    except Exception:
      print('mkdir:  cannot create directory \'' + newDirect + '\': Directory or File already exists\n')
  return
