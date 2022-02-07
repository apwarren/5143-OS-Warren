#Finished for Now
import os

def mkdir(params):
  errorMessages = ''
  
  for newDirect in params:
    try:
      os.mkdir(newDirect)
    except Exception:
      errorMessages += 'mkdir:  cannot create directory \'' + newDirect + '\': File exists\n'
  
  #Show errors to the user if there are any
  if(errorMessages != ''):
    return errorMessages
    
  #No errors occured
  return
