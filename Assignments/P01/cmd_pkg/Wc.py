#Finished for now
import os

def wc(params):

  if(len(params) > 1 and params[0][0] == '-'):
    flags = params[0]
    params =  params[1:]
    
  else:
    #Default is to show all flags
    params = params[0:]
    flags = '-lwm'

  results = ''
  Count = {
            'Lines'  : 0,
            'Words' : 0,
            'Charas': 0,
          }
  for files in params:
    try:
      with open(files) as f:
        file = f.read()

        if('l' in flags):
          Lines = (len(file.split('\n')) - 1)
          Count['Lines'] += Lines
          results += '\t' + str(Lines)

        if('w' in flags):
          file = file.replace('\n', ' ')
          Words = (len(file.split()))
          Count['Words'] += Words
          results += '\t' + str(Words)

        if('m' in flags):
          Charas = (len(file))
          Count['Charas'] += Charas
          results += '\t' + str(Charas)
          
        #We are piping so we don't want to show a file name
        if(files == "__piper"):
          results += '\n'
        else:
          results += ' ' + files + '\n'
    except Exception:
        if(files in os.listdir('.')):
          results += "wc: " + files + ": Is a directory\n"
          for flag in range(len(flags) - 1):
            results += '\t0'
          results += ' ' + files + '\n'
          
        else:
          results += "wc: " + files + ": No such file or directory\n"

  #Display Cummulative Results
  if(len(params) > 1):
    if('l' in flags):
      results += '\t' + str(Count['Lines'])
    if('w' in flags):
      results += '\t' + str(Count['Words'])
    if('m' in flags):
      results += '\t' + str(Count['Charas'])
      
    results += ' total'
  return results