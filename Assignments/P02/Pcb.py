class pcb:
  def __init__(self,line):
    data = line.strip().split()

    self.arrivalTime = int(data[0])    # Process arrival time
    self.pid = int(data[1])            # Process ID
    self.priority = int(data[2] .strip('p'))      # Priority
    self.CPUWaitTime = 0          # Time in ready queue
    self.IOWaitTime = 0           # Time in wait queue
    self.TotalCPUTime = 0             #Total time in cpu
    self.TotalIOTime = 0              #Total time in I/O
    
    self.Terminated = 0           # Time process terminated 
    self.TurnAroundTime = 0       # Time from start to finish
    
    self.cpuBursts = []           # list of cpu bursts
    self.ioBursts = []            # list of IO bursts

    # load cpu bursts from the `data` list by slicing
    # past the first 3 values and then grabbing every other value
    for i in range(3, len(data), 2):
      self.cpuBursts.append(int(data[i]))
      self.TotalCPUTime += self.cpuBursts[-1]

    # same as above, but starts at location 1 instead of zero so
    # it grabs IO bursts, and not cpu bursts
    for i in range(4,len(data),2):
      self.ioBursts.append(int(data[i]))
      self.TotalIOTime += self.ioBursts[-1]

  def getAT(self):
      """
      Returns the time process's arrival time
      """
      return self.arrivalTime

  def decrementCpuBurst(self):
      self.cpuBursts[0] -= 1
  
  def getCPUBurst(self):
      if(self.cpuBursts == []):
          return None
      else:
        return self.cpuBursts[0]

  def nextCPUBurst(self):
      del self.cpuBursts[0]

  def decrementIOBurst(self):
      self.ioBursts[0] -= 1
  
  def nextIOBurst(self):
      del self.ioBursts[0]

  def getIOBurst(self):
      if(self.ioBursts == []):
          return None
      else:
        return self.ioBursts[0]

  def incrCPUWait(self):
      self.CPUWaitTime += 1

  def incrIOWait(self):
      self.IOWaitTime += 1

  def getCPUWait(self):
      return self.CPUWaitTime

  def getIOWait(self):
      return self.IOWaitTime

  def setTAT(self, clock):
      self.TurnAroundTime = clock - self.arrivalTime
    
  def getTAT(self):
      return self.TurnAroundTime

  def getTotalCPUTime(self):
      return self.TotalCPUTime

  def getTotalIOTime(self):
      return self.TotalIOTime
  
  def decrementTotalCPUTime(self):
      self.TotalCPUTime -= 1

  def decrementTotalIOTime(self):
      self.TotalIOTime -= 1

  def getPriority(self):
      return self.priority

  def getPid(self):
      return self.pid

  def __str__(self):
    """ Prints a "process" out in a readable format. Feel free to
        change the format to whatever you see fit.
    """
    s = f'At: {self.arrivalTime}, Pid: {self.pid}, Priority: {self.priority}\n'
    s += f'CpuBursts: {self.cpuBursts} , \nIoBursts: {self.ioBursts}\n'
    s += f'CPUWaitTime: {self.CPUWaitTime} , IOWaitTime: {self.IOWaitTime}\n'
    return s


if __name__ == '__main__':
    selfing = pcb('1 2 3 4 5 6 7 8 9 10 11 12')
    print(selfing)
    print(selfing.getTotalCPUTime())
