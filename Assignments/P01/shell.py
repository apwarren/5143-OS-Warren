#!/usr/local/bin/python3
import sys
sys.path.append('/Users/allyw/source/VScode/CMPS 5143-OS/5143-OS-Warren/Assignments/P01/cmd_pkg')
from cmd_pkg import *

#Create getch
getch = Getch()

#Get prior history from file
with open('history') as f:
  history = f.readlines()

commands = {}


#Make dictionary containing all keys
with open("cmd_pkg/__init__.py", "r") as f:
  for item in f.readlines():
    key = item.split()[-1]
    commands[key] = eval(key)

#Get first input from user
print('% ', end = '', flush = True)
command = ''
chara = getch()
while(chara != '\r'):
  if(chara == '\x7f'):
    command = command[:-1]
    print('\b  \b\b', end = '', flush = True)
  elif(chara.isprintable()):
    command += str(chara)
  else:
      #Don't do anything if keys are pressed
      if(chara == '\x1b'):
          chara = getch()
          chara = getch()
          chara = getch()
      continue
  print(chara, end = '', flush = True)
  chara = getch()
print()
#------end of getching
  
history.append(command + '\n')
allCommands = []
redirection = []


while(True):
  #Load command from history
  if('!' in command):
    try:
      line = int(command[1:])
      command = history[line]
    except Exception:
      print('bash: history: numeric argument required')
      #Get new input from user
      print('% ', end = '', flush = True)
      command = ''
      chara = getch()
      while(chara != '\r'):
        if(chara == '\x7f'):
          command = command[:-1]
          print('\b  \b\b', end = '', flush = True)
        elif(chara.isprintable):
          command += chara
        else:
            #Don't do anything if keys are pressed
            if(chara == '\x1b'):
                chara = getch()
                chara = getch()
                chara = getch()
            continue
        print(chara, end = '', flush = True)
        chara = getch()
      print()
      continue

  if('>' in command):
    #We want to append to a file
    command = command.split('>')
    redirection = command[1:]
    command = command[0]

  if('<' in command):
    command = command.split('<')
    command = ''.join(command)
  
  #Check for piping
  if('|' in command):
    #We can pipe as much as we want
    allCommands = command.split('|')
    command = allCommands[0]
    del allCommands[0]
  #-------done with pipe checking------


  command = command.split()
  cmd = command[0]

  try:
    params = command[1:]
  except Exception:
    params = None

  if(cmd == 'exit'):
    with open("history", 'w') as h:
      h.write(''.join(history))
    sys.exit(0)

  elif(cmd == 'history'):
    result = '\n'.join(history)
    
  #We are not exiting program
  else:
    try:
      result  = commands[cmd](params)
    except Exception:
      result = commands[cmd]()

  #Still piping
  if(len(allCommands) > 0):
    if(result is not None):
      with open ('__piper', 'w') as f:
        f.write(result)
      allCommands[0] += ' __piper'
      
    if(len(allCommands) == 1):
      command = allCommands[0]
      allCommands = []
    else:
      command = '|'.join(allCommands)
    continue

  #Moving on to next command/Not piping
  else:       
    #Want to store output into a file
    if(result is not None):
      if(len(redirection) > 0):
        file = redirection[-1].strip()
        #write to a file
        if len(redirection) == 1:
          with open(file, 'w') as f:
            f.write(result)
        else:
          with open(file, 'a') as f:
            f.write(result)
        redirection = ''
      else:
        print(result)   
        
    #Get next input from user
    print('% ', end = '', flush = True)
    command = ''
    chara = getch()
    while(chara != '\r'):
      if(chara == '\x7f'):
        command = command[:-1]
        print('\b  \b\b', end = '', flush = True)
      elif(chara.isprintable):
        command += chara
      else:
        #Don't do anything if keys are pressed
        if(chara == '\x1b'):
            chara = getch()
            chara = getch()
            chara = getch()
        continue
      print(chara, end = '', flush = True)
      chara = getch()
    print()
    history.append(command + '\n')