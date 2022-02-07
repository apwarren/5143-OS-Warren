
def tail(params):
  try:
    if('-n' in params):
      #We are expecting a number after the dash
      size = int(params[-1])
      file = params[0]

    else:
      size = 10
      file = params[0]

    with open(file) as f:
        display = f.readlines()[-size:]
        
    return '\n'.join(display)

  except Exception:
    return('head: cannot open file for reading. Please check your command and try again')



