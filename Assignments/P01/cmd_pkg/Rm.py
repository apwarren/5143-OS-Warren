import os
import re

def rm(params):
  """   
    NAME
        rm - Remove a set of given files from the directory
    SYNOPSIS
        rm FILE
    DESCRIPTION
        This command takes a given file and permanently removes it from
        the directory. The command can delete multiple files at a time
        as well as takes wild card commands such that it will perform
        a partial match to file names and delete any aligning files
        as well. This command cannot delete directories unless the flag
        -r is called. This flag will recursively delete everything inside
        of the directory and then once its contents have been emptied it will
        delete the directory as well.
    USAGE
        rm FILE
          --Delete FILE from the directory
        rm FILE1 FILE2
          --Delete both FILE1 and FILE2 from the directory
        rm *FILE
          --Delete all files that end with FILE from the directory
        rm FILE*
          --Delete all files that begin with FILE from the directory
        rm FI*LE
          --Delete all files that begin with FI and end with LE from the directory

  """
  #Error checking
  #--------------------
  #No files were given to be deleted
  if(len(params) == 0):
    print('rm: missing file operand')
    return

  #A flag was passed in but no file names to be deleted
  elif(len(params) == 1 and '-' in params[0]):
    print('rm: missing file operand after \'' + params[0] + '\'')
    return

  #A flag was passed to be used for recursive removal
  elif('-' in params[0]):
    flags = params[0]
    original = params[1:]
    
  else:
    #Default is no flags passed
    original = params
    flags = ''

  #Get collection of all files needed to be removed
  allFile = []
  #Use regex to grab all wild card files
  RegexFile = []
  for origin in original:
    #Build regex string to compare with future files
    if('*' in origin):
      wild = origin
      wild.replace('.', '\.')
      re.split('(\*)', wild)
      origin = '^'
      for section in wild:
        if section == '*':
          origin += '.*'
        else:
          origin += section
    #Add newly created regex string to a list to check all files
    RegexFile.append(origin)   

    #Check entire directory for matches to get all files to be removed
    listing = os.listdir('.')
    for file in RegexFile:
      for lists in listing:
        #The wildcard or filename matches with a file in the directory
        if(re.match(file, lists)):
          allFile.append(lists)   
  #Now get ready to remove all files from the directory
  try:
    for file in allFile:
      #we plan to delete an entire directory so use recursion
      if('r' in flags):
        #Current item is a directory
        if(os.path.isdir(file)):
          if(len(os.listdir(file)) > 0):
            direct = os.getcwd()
            #Get everything inside of the directory
            newparams = os.listdir(file)
            #Remove everything inside of the directory recursively
            newparams.insert(0, '-r')
            os.chdir(file)
            rm(newparams)
            os.chdir(direct)
          else:
            os.rmdir(file)
        else:
          #Item was a file and can just be simply removed
          os.remove(file)

        #Directory has now been emptied and can be deleted
        os.rmdir(file)

      #We do not plan to use recursion and just want to delete files
      else:
        #Item is a directory so we can't delete it
        if(os.path.isdir(file)):
          print('rm: cannot remove \'' + file + '\': Is a directory')
        else:
          #Get rid of file in the directory
          os.remove(file)
    return  

  #An error occured when trying to erase the given items
  except Exception:
    return ('rm: cannot remove \'' + file + '\': No such file or directory')