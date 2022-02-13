import os

def wc(params):
  """   
    NAME
        wc - Prints out a count of lines, words, or characters
    SYNOPSIS
        wc FILE1
    DESCRIPTION
        This command takes a given number of files and prints out
        the count for how many lines, words, and characters exist
        within the file. The user is also able to pass in flags
        in order to only display specific counters as well.
        -l will print the number of lines, -w will print the
        nunber of words, and -m will count the number of characters.
        If multiple files are passed to the command, each one will
        display its counters with its file name.
    USAGE
        wc FILE1
          --return the number of lines, words, and characters in FILE1
        wc FILE1 ... FILEN
          --return the number of lines, words, and characters in FILE1 to FILEN
        wc -l FILE1
          --return just the number of lines in FILE1
        wc -w FILE1
          --return just the number of words in FILE1
        wc -m FILE1
          --return just the number of characters in FILE1
        wc -lwm FILE1
          --return the number of lines, words, and characters in FILE1
  """
  #Flags were passed to the command
  if(len(params) > 1 and '-' in params[0]):
    flags = params[0]
    params =  params[1:]
  
  #Default is to show all three counters to the user
  else:
    #Default is to show all flags
    params = params[0:]
    flags = '-lwm'

  results = ''
  #Get the counts for the lines words and charas
  #Also keep a total count for if multiple files are read
  Count = {
            'Lines'  : 0,
            'Words' : 0,
            'Charas': 0,
          }

  #Traverse all files user gives
  for files in params:
    try:
      #Open and store file's contents
      with open(files) as f:
        file = f.read()

        #User wants to see how many lines are in the file
        if('l' in flags):
          Lines = (len(file.split('\n')) - 1)
          Count['Lines'] += Lines
          results += '\t' + str(Lines)

        #User wants to see how many words are in the file
        if('w' in flags):
          file = file.replace('\n', ' ')
          Words = (len(file.split()))
          Count['Words'] += Words
          results += '\t' + str(Words)

        #User wants to see how many characters are in the file
        if('m' in flags):
          Charas = (len(file))
          Count['Charas'] += Charas
          results += '\t' + str(Charas)
          
        #We are piping so we don't want to show a file name
        if(files == "__piper"):
          results += '\n'
        #Show file name if multiple files are being read
        else:
          results += ' ' + files + '\n'

    #Error checking
    except Exception:
      #Can't get the word count of a directory
      if(files in os.listdir('.')):
        print("wc: " + files + ": Is a directory\n")
        #A directory contains 0 of all counters
        for flag in range(len(flags) - 1):
          results += '\t0'

        results += ' ' + files + '\n'

      #THe file given by the user does not exist in the current directory
      else:
        print("wc: " + files + ": No such file or directory\n")

  #Display Cummulative Results if multiple files were passed
  if(len(params) > 1):
    if('l' in flags):
      results += '\t' + str(Count['Lines'])
    if('w' in flags):
      results += '\t' + str(Count['Words'])
    if('m' in flags):
      results += '\t' + str(Count['Charas'])
      
    results += ' total'
    
  return results