#Finished for Now
import os

def cat(params):
  """   
    NAME
        cat - concatenate files and print on the standard output screen to the user
    SYNOPSIS
        cat [OPTION]... [FILE]...
    DESCRIPTION
        Concatenate FILE(s) to standard output terminal screen.
        Can display multiple files at a time
    USAGE
        cat FILE
          --display one file given its name
        cat FILE1 FILE2 . . . 
          --display multiple files one after the other given their names
        --help display this help and exit
        --version
                output version information and exit
  """
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