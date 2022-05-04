
class pcb:
  """   
    NAME
        pcb - Instance of a Process Control Block

    DESCRIPTION
        This class creates an instance of a process control block in 
        which the pcb holds the time it arrives, its unique id, 
        what priority it holds within the simulation if needed,
        how long it has had to wait to access a cpu, and io respectively.
        It also contains the time it was in the cpu and io device and
        when the process finished and was terminated. Finally it holds 
        each section of cpu and io bursts and the overall Turn Around Time
        of the pcb.
        
    ATTRIBUTES
        arrivalTime    :   int
            --Time pcb came into the simulation
        pid :   int
            --Unique id given to the pcb
        priority    :   int
            --How much pcb should be prioritized if needed. The smaller the number the less important
        CPUWaitTime : int
            --How long the pcb has had to wait for cpu access
        IOWaitTime  :   int
            --How long the pcb has had to wait for io access
        TotalCPUTime    :   int
            --How long the pcb will need to be on the cpu before terminating
        TotalIOTime :   int
            --How long the pcb will need to be on the io device before terminating
        Terminated  :   int
            --Time of whih the pcb finished running and terminated
        TurnAroundTime  :   int
            --Time from start to finish the pcb was running in the simulation
        cpuBursts   :   list
            --List of all cpu bursts the pcb needs to run through the cpu
        ioBursts    : list
            --List of all io bursts the pcb needs to run throught an io device
    """
  def __init__(self,line):
    data = line.strip().split()              #Get the pcb's information and divide it up

    self.arrivalTime = int(data[0])          # Process arrival time
    self.pid = int(data[1])                  # Process ID
    self.priority = int(data[2] .strip('p')) # Priority
    self.CPUWaitTime = 0                     # Time in ready queue
    self.IOWaitTime = 0                      # Time in wait queue
    self.TotalCPUTime = 0                    #Total time in cpu
    self.TotalIOTime = 0                     #Total time in I/O
    
    self.Terminated = 0                      # Time process terminated 
    self.TurnAroundTime = 0                  # Time from start to finish
    
    self.cpuBursts = []                      # list of cpu bursts
    self.ioBursts = []                       # list of IO bursts


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
      """
      Decreases the current cpu burst amount by one. 
      One clock tick has occured will on the cpu.
      """
      self.cpuBursts[0] -= 1
  
  def getCPUBurst(self):
      """
      Returns current cpu burst pcb is on. If none then return None instead.
      """
      if(self.cpuBursts == []): #No more cpu bursts
          return None
      else:
        return self.cpuBursts[0]

  def nextCPUBurst(self):
      """
      Pcb finished the last cpu bursts, so move on to the next one.
      """
      del self.cpuBursts[0] #Last cpu burst is empty so remove it

  def decrementIOBurst(self):
      """
      Decreases the current io burst amount by one. 
      One clock tick has occured while on an io device.
      """
      self.ioBursts[0] -= 1
  
  def nextIOBurst(self):
      """
      Pcb finished the last io burst, so move on to the next one.
      """
      del self.ioBursts[0]  #Last io burst is at 0 so remove it

  def getIOBurst(self):
      """
      Returns current io burst pcb is on. If none then return None instead.
      """
      if(self.ioBursts == []):  #No more io bursts are in the pcb
          return None
      else:
        return self.ioBursts[0]

  def incrCPUWait(self):
      """
      Increases the current time that pcb has needed a cpu by one. 
      One clock tick has occured while in the ready queue.
      """
      self.CPUWaitTime += 1

  def incrIOWait(self):
      """
      Increases the current time that pcb has needed an io by one. 
      One clock tick has occured while in the waiting queue.
      """
      self.IOWaitTime += 1

  def getCPUWait(self):
      """
      Returns the time process's time in the ready queue overall
      """
      return self.CPUWaitTime

  def getIOWait(self):
      """ 
      Returns the time process's time in the waiting queue overall
      """
      return self.IOWaitTime

  def setTAT(self, clock):
      """ 
      Sets the pcb's Turn Around Time after entering Terminated Queue
      """
      self.TurnAroundTime = clock - self.arrivalTime
    
  def getTAT(self):
      """ 
      Returns the time process's Turn Around Time
      """
      return self.TurnAroundTime

  def getTotalCPUTime(self):
      """ 
      Returns the time process's time needed on the cpu overall
      """
      return self.TotalCPUTime

  def getTotalIOTime(self):
      """ 
      Returns the time process's time needed on the io device overall
      """
      return self.TotalIOTime
  
  def decrementTotalCPUTime(self):
      """
      Decreases the current total cpu time amount by one. 
      One clock tick has occured while on a cpu.
      """
      self.TotalCPUTime -= 1

  def decrementTotalIOTime(self):
      """
      Decreases the current io total time amount by one. 
      One clock tick has occured while on an io device.
      """
      self.TotalIOTime -= 1

  def getPriority(self):
      """ 
      Returns the process's set priority level
      """
      return self.priority

  def getPid(self):
      """ 
      Returns the id of the pcb
      """
      return self.pid

  def __str__(self):
    """ 
    Prints a "process" out in a readable format. 
    """
    s = f'At: {self.arrivalTime}, Pid: {self.pid}, Priority: {self.priority}\n'
    s += f'CpuBursts: {self.cpuBursts} , \nIoBursts: {self.ioBursts}\n'
    s += f'CPUWaitTime: {self.CPUWaitTime} , IOWaitTime: {self.IOWaitTime}\n'
    return s


# if __name__ == '__main__':
#     selfing = pcb('1 2 3 4 5 6 7 8 9 10 11 12')
#     print(selfing)
#     print(selfing.getTotalCPUTime())
