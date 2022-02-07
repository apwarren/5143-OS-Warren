#Finished! very proud of this one
import os
import re

def rm(params):
  originalPath = os.getcwd()
  #Error checking
  if(len(params) == 0):
    return('rm: missing file operand')

  if(len(params) == 1 and '-' in params[0]):
    return('rm: missing file operand after \'' + params[0] + '\'')

  if(len(params) > 3 or (len(params) == 2 and '-' not in params[0])):
    return('mv: too many arguments')

  if(len(params) > 1 and params[0][0] == '-'):
    flags = params[0]
    original = params[1]
    
  else:
    #Default is no flags
    original = params[0]
    flags = ''

  try:
    #we plan to delete an entire directory
    if('r' in flags):
      #Build regex string to compare with future 
      if('*' in original):
        wild = original
        wild.replace('.', '\.')
        re.split('(\*)', wild)
        original = '^'
        for section in wild:
          if section == '*':
            original += '.*'
          else:
            original += section
      #Check entire directory for matches
        listing = os.listdir('.')
        for lists in listing:
          if(re.match(original, lists)):
            if(os.path.isdir(lists)):
              rm(['-r', lists])
            else:
              rm([lists])
        os.chdir(originalPath)
        return

      parent = os.getcwd()
      os.chdir(original)
      insideDir = os.listdir()
      while(len(insideDir) > 0):
        if(os.path.isdir(insideDir[0])):
          newparams = ['-r ', insideDir[0]]
          rm(newparams)
        else:
          rm([insideDir[0]])
        del insideDir[0]
      os.chdir(parent)
      os.rmdir(original)

    else:
      #We plan to move to another directory without deleting it
      if('/' in original):
        originPath = original.split('/')
        original = originPath[-1]
        originPath = originPath[:-1]
        originPath = '/'.join(originPath)
        os.chdir(originPath)

      #Build regex string to compare with future 
      if('*' in original):
        wild = original
        wild.replace('.', '\.')
        re.split('(\*)', wild)
        original = '^'
        for section in wild:
          if section == '*':
            original += '.*'
          else:
            original += section
      #Check entire directory for matches
        listing = os.listdir('.')
        for lists in listing:
          if(re.match(original, lists)):
            if(os.path.isdir(lists)):
              print('rm: cannot remove \'' + lists + '\': Is a directory')
            else:
              rm([lists])
        os.chdir(originalPath)
        return
        
      #Get rid of file at its found location 
      os.remove(original)

      #Go back to orignal directory
      os.chdir(originalPath)

  except Exception:
    return ('rm: cannot remove \'' + original + '\': No such file or directory')