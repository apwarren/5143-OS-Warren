from Cat import cat
def sort(params):
  try:
    allInfo = cat(params)
    if('cat:' in allInfo and 'No such file or directory' in allInfo):
      raise Exception
    allInfo = allInfo.split('\n')
    del allInfo[-1:]
    allInfo.sort()
    return '\n'.join(allInfo)
  except Exception:
    return 'sort: cannot read: No such file within command'
