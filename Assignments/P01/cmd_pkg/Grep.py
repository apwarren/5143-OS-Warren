
def grep(params):
  if('-' in params[0]):
    flags = params[0]
    keyword = params[1]
    files = params[2:]

  else:
    flags = ''
    keyword = params[0]
    files = params[1:]

  listing = []
  #Only want the file name so we don't need to look for every line
  if('l' in flags):
    for file in files:
      try:
        with open(file) as f:
          if(keyword in f.read()):
            listing.append(file)
      except Exception:
        error = 'grep: ' + file + ': No such file'
        listing.append(error)
        
    return '\n'.join(listing)

  else:
    for file in files:
      try:
        with open(file) as f:
          lines = f.readlines()
          for line in lines:
            display = ''
            if(keyword in line):
              if len(files) > 1:
                display += file + ': '
              display += line
              listing.append(display)
      except Exception:
        error = 'grep: ' + file + ': No such file'
        listing.append(error)

  return ''.join(listing)

