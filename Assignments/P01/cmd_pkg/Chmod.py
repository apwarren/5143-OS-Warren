import os
def chmod(params):
  #Number is given in octal so store it as octal
  permissions = int(params[0], 8)
  file = params[1]

  os.chmod(file, permissions)
  return