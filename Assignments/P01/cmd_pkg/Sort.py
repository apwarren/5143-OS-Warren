from .Cat import cat
def sort(params):
  """   
    NAME
        sort - Sort the lines of all given files line by line
    SYNOPSIS
        sort FILE
    DESCRIPTION
        This command takes a given file and separates it line by line.
        It will then return all of these lines in alphabetical order.
        If more than one file is given to the command, it will
        sort all the files without taking into consideration
        one from the other. In short, the files are not separated
        when sorted.
    USAGE
        sort FILE
          --sort the FILE's contents line by line
        sort FILE1 FILE2
          --Sort FILE1 and FILE2 alphabetically line by line without splitting files
  """
  #Read from every file given that exists
  try:
    #Get all file contents. cat returns all file contents in one bundle
    allInfo = cat(params)
    #Make all content into a list separated by each line
    allInfo = allInfo.split('\n')
    #Last line is just a blank line so remove it
    del allInfo[-1:]
    #Sort all of these lines alphabetically
    allInfo.sort()
    return '\n'.join(allInfo)
    
  #File given does not exist
  except Exception:
    print('sort: cannot read: No such file within command')
