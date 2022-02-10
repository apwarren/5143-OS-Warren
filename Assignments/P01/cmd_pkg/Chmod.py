import os
def chmod(params):
  """   
    NAME
        chmod - change modify permission for a given file or directory
    SYNOPSIS
        chmod xxx PATH
    DESCRIPTION
        This command will take the given directory or file and change
        its read, write, and execute permissions given an octal value.
        If the user is to call for long listing they should be able
        to view this change in said listing. The octal value should be
        represented to three place values in which the for a random
        value abc, a represents the roots permissions to this file;
        b represents the permission of the currently logged-in user
        for the item; lastly, c represents the permissions of other
        users on this item.
    USAGE
        chmod xxx FILE
          --Change the mode and permissions for a file given the octal value xxx
        chmod xxx DIRECTORY
          --Change the mode and permission for a directory given the octal value xxx
          
  """
  
  #Number is given in octal so convert and store it as decimal
  permissions = int(params[0], 8)
  #The desired file/directory should be the second item of the parameter list
  file = params[1]
  #change the mode of permissions for given file/directory
  os.chmod(file, permissions)

  #Return nothing to the user
  return