from .Rm import rm

def rmdir(params):
  """   
    NAME
        rmdir - Remove a directory
    SYNOPSIS
        rmdir DIRECTORY
    DESCRIPTION
        This command takes a given directory and permanently removes it. 
        The command can delete multiple directories at a time if desired
        as well as takes wild card commands such that it will perform
        a partial match to directory names. This flag will recursively 
        delete everything inside of the directory and then once its 
        contents have been emptied it will delete the directory as well.
        rm DIRECTORY
          --Delete DIRECTORY from the system
        rm DIRECTORY1 DIRECTORY2
          --Delete both DIRECTORY1 and DIRECTORY2
  """
  #Pass in every given directory name and call the remove function recursively
  direct = params
  direct.insert(0, '-r')
  #rm will delete the directory and all its contents
  rm(direct)
  return