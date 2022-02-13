
def tail(params):
  """   
    NAME
        tail - Print the last few lines of a given file
    SYNOPSIS
        tail FILE1
    DESCRIPTION
        This command takes a given number of files and prints out
        the last few lines contained within each file. If the user
        uses the flag -n #, then the command will print out # number
        of lines from each file, otherwise it will print out ten
        lines as the default.
    USAGE
        tail FILE1
          --return the last 10 lines from FILE1
        tail FILE1 ... FILEN
          --return the last 10 lines from FILE1 to FILEN each
        tail -n x FILE1
          --return the last x lines from FILE1
        tail -n x FILE1 ... FILEN
          --return the last x lines from FILE1 to FILEN each
  """
  try:
    tailing = []
    #We want to show a specific number of lines given
    if('-n' in params):
      #We are expecting a number after the flasg
      index = params.index('-n') + 1
      size = int(params[index])   #Get how many lines the user wants to see
      del params[index -1]        #Remove flag from the list
      del params[index - 1]       #Remove the index size from the list
      files = params              #Everything left in parameters should be files

    #Default viewing size is 10 lines
    else:
      size = 10
      files = params

    #Get all given files and display each one's 'tail'
    for file in files:
      with open(file) as f:
          display = f.readlines()[-size:]  #Only store the last desired lines
      if(len(files) > 1):
        name = '==>' + file + '<==\n'       #State which file it is if more than one
        display.insert(0, name)             #File name should be seen first
      tailing.append(''.join(display))      #Add to overall listing
    
    return '\n\n'.join(tailing)             #Compact every into one string to return

  except Exception:
    return('tail: cannot open file for reading. Please check your command and try again')
