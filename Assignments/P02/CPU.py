from Pcb import pcb
from rich.table import Table
from rich.panel import Panel

class Cpu:
    """   
    NAME
        Cpu - Rich table containing all simulated instances of a CPU

    DESCRIPTION
        Table builder to create a table displaying all instances of cpus 
        being simultated for the scheduling algorithm. A list of the pcbs
        on the cpu is given and the table will display each one's process id
        and current cpu burst time.
        
    ATTRIBUTES
        cpus    :   list
            --list containing all pcbs currently on the cpu
    """
    def __init__(self, cpus):
        self.cpu = cpus

    def build_table(self):
        """   
        NAME
            build_table - Table created based on class attributes

        DESCRIPTION
            Table builder to create a table displaying all instances of cpus 
            being simultated for the scheduling algorithm. A list of the pcbs
            on the cpu is given and the table will display each one's process id
            and current cpu burst time. CPUS are shown in each one's own column for readability.
        
        PARAMETERS
            None

        RETURNS
            table   : Table
                --returns the created table instance
        """
        
        table = Table(title="CPUs")             #Create table
        size = len(self.cpu)                    #Get size of the table

        #Upper right rorner Should not have anything in it
        table.add_column('  ', justify='center', no_wrap=True)

        #Add a column for every cpu given in the list
        for cpus in range(size):
            table.add_column(f"CPU {cpus + 1}", justify="center", style="cyan", no_wrap=True)
        
        
        ids = []
        bursts = []

        #Get each cpu's process and burst amount
        for block in self.cpu:
            if(block is not None):                           #There is a pcb currently being run on the cpu
                ids.append(f'{block.getPid()}')
                bursts.append(f'{block.getCPUBurst()}')
            else:
                ids.append('-----')                          #No process is currently running on cpu
                bursts.append('-----')

        table.add_row('Process ID', *ids, style='orange3')   #First row contains each cpu's process id
        table.add_row('CPU Burst', *bursts, style='yellow3') #Second row contain's each cpu's burst amount
        
        return table

    def __rich__(self) -> Panel:
        return Panel(self.build_table())
