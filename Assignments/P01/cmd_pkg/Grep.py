
def grep(params):
  """   
    NAME
        grep - Find the lines or files that contain a keyword within it
    SYNOPSIS
        grep KEYWORD FILE1 ... FILEN
    DESCRIPTION
        This command takes a given keyword that the user is looking for and then
        traverses through all files that the user gives to the command to see
        where in all files this keyword occurs. If the user does not pass any
        flags to the command then the command will show every entire line that
        the keyword occurs in. If the user passes -l to the command then it will
        not print out every line but rather just state which of the given files
        contains the keyword. It does not state how many times the word occurs within
        each file just that it does occur.

    USAGE
        grep KEYWORD FILE1 ... FILEX
          --Look through all files from FILE1 to FILEX and print each line KEYWORD appears
        grep -l KEYWORD FILE1 ... FILEX
          --Look through all files from FILE1 to FILEX and print each file name that KEYWORD appears

  """
  #The user has input flags that need to be checked
  if('-' in params[0]):
    flags = params[0]     #The user wants a specific output
    keyword = params[1]   #Word to be found within the file
    files = params[2:]    #All files that need to be looked through

  #User just wants standard grep
  else: 
    flags = ''            #No flags were given in the command
    keyword = params[0]   #Word to be found within the file
    files = params[1:]    #All files that need to be looked through

  listing = []

  #Only want the file name so we don't need to look for every line
  if('l' in flags):
    #Traverse every file
    for file in files:
      #Open the file and read it if it exists
      try: 
        with open(file) as f:
          if(keyword in f.read()):
            listing.append(file)                  #File contains the word so store name of file
      #The file does not exist within the directory and thereby cannot be opened
      except Exception:
        print('grep: ' + file + ': No such file') #Tell user the file does not exist

    #Return all file names that contain the keyword
    return '\n'.join(listing)

  #The user wants the actual lines containing the keyword
  else:
    for file in files:
      #If the file, exists read through it
      try:
        with open(file) as f:
          lines = f.readlines()
          #Get each individual line of a file
          for line in lines:
            display = ''
            if(keyword in line):        #The word exists on a line
              if len(files) > 1:        #Tell which file it came from if more than one file was passed
                display += file + ': ' 
              display += line
              listing.append(display)   #Add to list of all valid lines
      #The file does not exist and cannot be opened
      except Exception:
        print('grep: ' + file + ': No such file')

  return ''.join(listing)

