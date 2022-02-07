#Finished for now!!! This was fun
import os
import time

def ls(params):
  if(params):
    if(params[0][0] == '-'):
      flags = params[0]
      if(len(params) == 1):
        paras = ['.']
      else:
        paras = params[1:]
    else:
      flags = ''
      paras = params
  else:
    #default is parent directory
    paras = ['.']
    flags = ''
  allOutput = ''
  for paths in range(len(paras)):
    item = paras[paths]
    if(os.path.isfile(item) or os.path.isdir(item)):
      pass
    else:
      allOutput += 'ls: cannot access \'' + item + '\': No such file or directory\n'
  paras = [i for i in paras if os.path.isdir(i) or os.path.isfile(i)]


  #Print out for all intended directories/files
  for paths in paras:
    if len(paras) > 1:
      allOutput += paths + ':\n'
    #Assume at first that user wants all files including hidden ones
    if(os.path.isdir(paths)):
      listing = os.listdir(paths)
      listing.insert(0, '.') #Parent directory
      listing.insert(1, '..') #Grandparent directory
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
        if(os.path.isfile(item)):
          longListing[-1:] = '-'
        else: #item is a directory
          longListing[-1:] = 'd'

        #Next display files permissions
        if(os.path.isdir(paths)):
          pathway = paths + '/' + item
        else:
          pathway = paths
        permission = bin(os.stat(pathway).st_mode)[-9:]
        for index in range(9):
          if(permission[index] == '1'):
            longListing[-1] += allAccess[index]
          else:
            longListing[-1] += '-'
        
        #Next get number of hardlinks attached to item
        longListing[-1] += ' '
        longListing[-1] += str(os.stat(pathway).st_nlink)

        #Next get user id of owner
        longListing[-1] += str(os.stat(pathway).st_uid)

        #And group id of owner
        longListing[-1] += ' '      
        longListing[-1] += str(os.stat(pathway).st_gid)

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
          longListing[-1] += size.rjust(5)

        #User does not want sizes to be human readable
        else:
          longListing[-1] += str(int(size)).rjust(5)

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
          index = listed % maxLines
          allFiles[index] += listing[listed] + '  '
        allOutput += ('\n'.join(allFiles))
      else:
        allOutput += ('\t'.join(listing))

    if(len(paras) > 1 and paths != paras[-1]):
      allOutput += '\n\n'

  return allOutput