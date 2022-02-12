from cmd_pkg import *

def help(params):
  """   
    NAME
        help - Print the head documentation of a given command
    SYNOPSIS
        COMMAND --help
    DESCRIPTION
        This command takes another given command and
        prints out its general description to allow
        the user to understand how to adequately use
        the command and what options the command may
        offer.
    USAGE
        COMMAND --help
          --returns COMMAND's documentation to the user
  """
  #Go to the function command and get its documentation
  return eval(params).__doc__