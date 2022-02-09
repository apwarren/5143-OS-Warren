#Finished
import os
from .getch import Getch

def less(params):
  try:
    with open(params[0], 'r') as f:
      lines = f.readlines()
    fileLength = len(lines)

    #We really only need to know how many rows the terminal size is so we ignore column size
    rows = os.get_terminal_size()[-1]
     #Convert sizing into integer values
    start = 0
    rows = int(rows) // 2
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
    return

  except:
    pass