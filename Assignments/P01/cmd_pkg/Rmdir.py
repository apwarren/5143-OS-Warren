#Finished, yes I took the easy way I just spent all my time on removing so I might as well use it
from Rm import rm

def rmdir(params):
  direct = params
  direct.insert(0, '-r')
  rm(direct)