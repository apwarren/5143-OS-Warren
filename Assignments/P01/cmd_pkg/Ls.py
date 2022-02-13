import os
import pwd
import grp
import time

def ls(params):
  """   
    NAME
        ls - Print out listing of all file and directories
    SYNOPSIS
        ls
    DESCRIPTION
        This command takes the command ls and displays a listing of
        all files and directories for a given directory. If no directory
        is provided then the command will assume you want a listing
        of the current directory. This command takes three flags as well.
        -l will provide a detailed long listing of all contents within the
        directory. -a will show all items within the directory including
        all hidden files and directories. and -h will show the size of the
        files and directories listed in a human readable format. All three
        of these commands can be used interchangably with all three being 
        independent of one another.
    USAGE
        ls
          --Print the names of all public files within the current directory
        ls -l
          --Print a detailed listing of all public files within current directory
        ls -a
          --Print the names of all files within the directory including hidden ones
        ls -h
          --Print any item sizes in a human readable format. Makes listing human readable
        ls -la
          --Print a detailed listing of all files within current directory including hidden ones
        ls -lh
          --Print a detailed listing of all public files within current directory with everything human readable
        ls -ah
          --Print the names of all files within the directory including hidden ones
        ls -lah
          --Print a detailed listing of all hidden and open files within current directory with everything human readable
        ls ... DIRECTORY
          --Print out the desired listing of a particular given directory according to given flags
  """
  #Separate parameters if parameters were given
  if(params):
    #Flags were passed to command
    if(params[0][0] == '-'):
      flags = params[0]

      if(len(params) == 1): #Only flags were passed and nothing else
        paras = ['.']       #Only look at current working directory

      else:                 #We are told what directories to list
        paras = params[1:]

    #No flags were passed to the command but there were directories
    else:
      flags = ''
      paras = params

  #No flags or directories were listed so default is ls
  else:
    #default is current working directory
    paras = ['.']
    flags = ''

  #Holder to store all information before returning
  allOutput = ''

  #Make sure all given parameters are valid besides flags
  for paths in range(len(paras)):
    item = paras[paths]
    if(os.path.isfile(item) or os.path.isdir(item)):
      pass
    #Print error for any items that are not valid within the parameter listing
    else:
      print('ls: cannot access \'' + item + '\': No such file or directory\n')
  #All paramters are now valid
  paras = [i for i in paras if os.path.isdir(i) or os.path.isfile(i)]


  #Print out for all intended directories/files
  for paths in paras:
    if len(paras) > 1:
      allOutput += paths + ':\n'

    #Assume at first that user wants all files including hidden ones at first
    if(os.path.isdir(paths)):
      listing = os.listdir(paths)
      listing.insert(0, '.')  #Parent directory
      listing.insert(1, '..') #Grandparent directory
      #Sort everything into alphabetical order ignoring special characters
      listing.sort(key=lambda y: y.strip('__').strip('.').lower())
    else:
      listing = [paths]

    #User just wants ls and no hidden files
    if('a' not in flags):
      listing = [i for i in listing if i.startswith('.') is False]

    #User wants long listing
    if('l' in flags):
      longListing = []
      #The order if an item were to get all permissions
      allAccess = 'rwxrwxrwx'
      for item in listing:
        #First determine if item is a file or directory
        if(os.path.isfile(item)): #Item is a file
          longListing[-1:] = '-'
        else: #item is a directory
          longListing[-1:] = 'd'

        #Next display files permissions
        if(os.path.isdir(paths)):
          pathway = paths + '/' + item
        else:
          pathway = paths

        #Get current item's permission value in binary
        permission = bin(os.stat(pathway).st_mode)[-9:]
        
        #default is rwxrwxrwx and we see where the 1's are for the binary value
        for index in range(9):
          if(permission[index] == '1'):   #The permission is granted
            longListing[-1] += allAccess[index]
          else:
            longListing[-1] += '-'        #The item does not have this position
        
        #Next get number of hardlinks attached to item
        longListing[-1] += ' '
        longListing[-1] += str(os.stat(pathway).st_nlink)

        # #Next get user id of owner
        userID = os.stat(pathway).st_uid
        longListing[-1] += ' ' + pwd.getpwuid(userID)[0]
        # #And group id of owner
        groupID = os.stat(pathway).st_gid
        longListing[-1] += ' ' + grp.getgrgid(groupID)[0]

        # Get size of current item
        # Check if user wants human readable sizing
        size = float(os.stat(pathway).st_size)
        if('h' in flags):
          for unit in ['B','K','M','G','T']:
            if size < 1024.0:
              if unit == 'B':
                #No need for decimal representation
                size = str(int(size))
              else:
                #Shorten number to one decimal place
                size = str("{:.1f}".format(size))
              #Add what unit number is in
              size += unit
              break
            else:
              size /= 1024.0
          #Add human readable size to file listing
          longListing[-1] += size.rjust(7)

        #User does not want sizes to be human readable
        else:
          longListing[-1] += str(int(size)).rjust(7)

        #Get last date of modification
        date = str(time.ctime(os.path.getmtime(pathway)))
        date = date.split()
        #Get month
        longListing[-1] += date[1].rjust(4)
        #Get day
        longListing[-1] += date[2].rjust(3)
        #Get time
        longListing[-1] += date[3][:-3].rjust(6)

        #Finally show the name of the file
        longListing[-1] += ' ' + item

        #Move on to next item to format
        longListing.append('')
      #Get rid of last unneccesary index
      del longListing[-1]

      #Return the long list and leave function
      allListed = 'total ' + str(len(longListing)) + '\n'
      allOutput += (allListed + '\n'.join(longListing))

    else:
      #User did not want long listing
      #5 files/directories per line
      maxLines = (len(listing) // 5)
      if(len(listing) > 5):
        allFiles = [''] * maxLines
        for listed in range(len(listing)):
          #Sort by columns in alphabetical order
          index = listed % maxLines
          #Make sure everything lines up with adequate spacing
          allFiles[index] += listing[listed].ljust(15) + '  '
        allOutput += ('\n'.join(allFiles))
      #Don't need to worry about column lining
      else:
        allOutput += ('\t'.join(listing))

    #If multiple directories are to be listed separate the lists notably
    if(len(paras) > 1 and paths != paras[-1]):
      allOutput += '\n\n'

  return allOutput