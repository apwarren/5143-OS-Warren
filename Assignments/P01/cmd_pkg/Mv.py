import os

def mv(params):
  """   
    NAME
        mv - Move contents from one file and put it into another file
    SYNOPSIS
        mv FILE1 FILE2
    DESCRIPTION
        This command takes two given files. The first file contains
        the contents of which the user wishes to move. Then the next
        item of the command is expected to be either another file,
        a name for a new file, or a directory. If the user wishes to
        move the first file into another existing file, then the system
        will erase the previous contents of the other file and replace it
        with the new given contents. If the user gives a name that is not
        currently that of an existing file then it will create a new file
        called by that given name and store the previous file's contents into
        it. Lastly if the user gives a directory for the second listing to store
        the item into and does not give a file name, then the system will copy and
        store file1's contents into that directory by creating a new file with the
        same name of the original file. After moving the content's to the new location,
        the original file will be removed and deleted from its directory as this is 
        not a copy but a replacement.
    USAGE
        mv FILE1 FILE2
          --Move everything from FILE1 and store it inside of FILE2. Then delete FILE1
        mv FILE1 NEWFILE
          --Copy everything from FILE1 and store it in a new file called NEWFILE. Delete FILE1
        mv FILE1 DIRECTORY
          --Copy everything from FILE1 and go to the given DIRECTORY and store it in a file called FILE1
          --Delete FILE1 from its original location.

  """
  #Store which directory we are currently in to go back at the end
  originalPath = os.getcwd()

  #Error checking
  #--------------------
  #No files were given to move to and from
  if(len(params) == 0):
    print('cp: missing file operand')

  #Only one file was given and we don't know where to move to
  elif(len(params) == 1):
    print('cp: missing destination file operand after \'' + params[0] + '\'')

  #More than two parameters were given and we can only move to and from one file each
  elif(len(params) > 2):
    print('cp: too many arguments')

  #We are able to move the file and send it elsewhere
  else:
    #First item should be the file to read from and second it where to go
    original = params[0]
    newFile = params[1]

    #Make sure the file path exists when reading contents
    try:

      #We plan to move to another directory to get file to read from
      if('/' in original):
        originPath = original.split('/')
        original = originPath[-1]         #Exsting file
        originPath = originPath[:-1]      
        originPath = '/'.join(originPath) #Path to move file to
        os.chdir(originPath)              #Go to the directory of where the file to read from is

      #Check to make sure a file is being copied and read/store its contents
      with open(original) as f:
        info = f.read()
      
      #Unlike copy we don't want the file to stay in the original location so remove it
      os.remove(original)

      #Go back to orignal directory we started at
      os.chdir(originalPath)

      #We plan to move to another directory to put contents into
      if('/' in newFile):
        newPath = newFile.split('/')
        newFile = newPath[-1]       #Name of file to place original inside of
        newPath = newPath[:-1]      #Path to store moved file into
        newPath = '/'.join(newPath)
        os.chdir(newPath)           #Go to the directory

      #moving to a directory not another file so go inside of said directory
      if(os.path.isdir(newFile)):
        os.chdir(newFile)

        #Not given a file name so name new file the same as the original one
        newFile = original
        
      #Move contents into new file
      with open(newFile, 'w') as f:
        f.write(info)

      #Go back to orignal directory and leave command
      os.chdir(originalPath)
      
    #An issue occurred and one of the given files is causing erros
    except Exception:
      
      #The file to move from exist but the command cannot move to new file
      if(os.path.exists(original)):
        return ('mv: cannot stat \'' + newFile + '\': No such file or directory')
      #The file to copy from does not exist and therefore we are unable to copy
      else:
        return ('mv: cannot stat \'' + original + '\': No such file or directory')
   