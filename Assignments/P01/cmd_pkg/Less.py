import os
from .getch import Getch

def less(params):
  """   
    NAME
        less - Print out part of a file when desired
    SYNOPSIS
        less FILE1
    DESCRIPTION
        This command takes a given file and only prints out partially
        what is within the file at a given time. By using certain keys
        that have been grabbed through getch, the command will traverse
        through the file based on what the user presses. For instance,
        using the up and down arrow keys will allow the user to move
        up and down a line in the file. Using space/f and 'b' will
        allow the user to move up and down 'pages' of the file. A
        page is considered to be the size of the terminal. The user
        can view all inner commands using 'h' which will allow them
        to view a guideline of all keys. Lastly, pressing 'q' will
        cause the command to finish and exit to let the user move
        on to a new command.
    USAGE
        less FILE1
          --Print the first several lines of FILE1 that fit within the terminal
          --Does not move on to a new shell command until Q is pressed
  """
  try:
    #Get and read every line in the file to be traversed through
    with open(params[0], 'r') as f:
      lines = f.readlines()

    #Get file size to know when to stop
    fileLength = len(lines)

    #We really only need to know how many rows the terminal size is so we ignore column size
    rows = os.get_terminal_size()[-1]

    #Convert sizing into integer values
    #Only show half of terminal size because for some reason the size is too big
    rows = int(rows) // 2
    #Start at the beginning of the file
    start = 0
    #The end of the display should initially be at the end of the terminal size
    end = rows

    #We plan to get user input without displaying it to the terminal
    getch = Getch()
    action = ''

    #Keep showing unless user specifically wants to quit
    while(action.lower() != 'q'):

      #Display portion of file
      for line in lines[start : end]:
        print(line)

      #Determine what the user wants to do now
      action = getch()

      #Move up and down by one line with the arrow keys
      if action in '\x1b':      # arrow key pressed
            null = getch()      # waste a character
            direction = getch() # grab the direction

            #Go back up one line of the file
            if direction in 'A':   # up arrow pressed
              # Makes sure we can actually move up and we aren't already at the top
              if(start > 0):
                start -= 1
                end -= 1
   
            if direction in 'B':    # down arrow pressed
              #Make sure we can still move down the file
              if(end < fileLength):
                start += 1
                end += 1
            else:
              continue
      #Show the help guideline window showing all commands      
      elif(action.lower() == 'h'):
        print('''
              \n
              Less Command Guide for Viewing File Partially:\n
              ==============================================\n
              press  'up arrow' | Move up one line\n
              press 'down arrow'| Move down one line\n
              press  'space bar'| Move forward one page\n
              press  'f' or 'F' | Move forward one page\n
              press  'b' or 'B' | Move backward one page\n
              press  's' or 'S' | Move to the beginning of the file\n
              press  'e' or 'E' | Move to the end of the file\n
              press  'q' or 'Q' | Exit Less command\n
              press  'h' or 'H' | Display help for commands\n
              ==============================================\n
              ------press any key to return to the file-----
              ''')
        action = getch()
        continue

      #Skip forward a page
      elif(action.lower() == 'f' or action == ' '):
        if(end < fileLength - rows):
          start += rows
          end += rows

      #Skip back a whole page.
      elif(action.lower() == 'b'):
        if(start >= rows):
          start -= rows
          end -= rows
        else:
          start = 0
          end = rows

      #Move to the end of the file
      elif(action.lower() == 'e'):
        start = fileLength - rows
        end = fileLength

      #Move to the beginning of the file
      elif(action.lower() == 's'):
        start = 0
        end = rows
    
    #Return all file contents for redirection purposes
    return ''.join(lines)

  #File could not be read
  except:
    print('less: File does not exist')