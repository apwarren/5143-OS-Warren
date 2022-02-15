import os
def rmdir(params):
  """   
    NAME
        rmdir - Remove a directory
    SYNOPSIS
        rmdir DIRECTORY
    DESCRIPTION
        This command takes a given directory and permanently removes it. 
        The command can delete any empty directory and remove it.
    USAGE
        rm DIRECTORY
          --Delete DIRECTORY from the system if it is empty
        rm DIRECTORY1 DIRECTORY2
          --Delete both DIRECTORY1 and DIRECTORY2 if they are empty
  """
  #Pass in every given directory name and remove all that exist
  directs = params
  for direct in directs:
    try:
        if len(os.listdir(direct)) == 0:
          #Directory is empty and can be deleted
          os.rmdir(direct)
        else:
          print('rmdir: \'' + direct + '\'Directory is not empty: Cannot be removed')
    except Exception:
      print('rmdir: \'', direct, '\': Directory does not exist')
  return