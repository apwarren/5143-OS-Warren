import subprocess

def who():
  """   
    NAME
        who - List users currently logged in
    SYNOPSIS
        who
    DESCRIPTION
        This command takes lists all user that are currently logged into
        the system.
    USAGE
        who
          --returns a list of user currently logged in
  """
  return(subprocess.check_output("who"))