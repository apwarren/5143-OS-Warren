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
  """
  allFiles = ''

  #Read from every given file the user wants 
  for files in params:
    #Open and read the file if it exists
    try:
      with open(files) as f:
        #cat wants the entire file's contents
        allFiles += f.read() + '\n'
      continue

    #The file does not exist in the directory or the object is not a file
    except Exception:
        if(os.path.isdir(files)):
          print("cat: " + files + ": Is a directory")
        else:
          print("cat: " + files + ": No such file or directory")
          
  #return all files content to the screen        
  return allFiles