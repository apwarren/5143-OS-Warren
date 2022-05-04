from Pcb import pcb
from rich.table import Table
from rich.panel import Panel

class IO:
    """   
    NAME
        IO - Rich table containing all simulated instances of IO Devices

    DESCRIPTION
        Table builder to create a table displaying all instances of io devices 
        being simultated for the scheduling algorithm. A list of the pcbs
        on the io device is given and the table will display each one's process id
        and current io burst time.
        
    ATTRIBUTES
        io    :   list
            --list containing all pcbs currently on an io device
    """
    def __init__(self, ios):
        self.io = ios
    
    def build_table(self):
        """   
        NAME
            build_table - Table created based on class attributes

        DESCRIPTION
            Table builder to create a table displaying all instances of ios 
            being simultated for the scheduling algorithm. A list of the pcbs
            on an io device is given and the table will display each one's process id
            and current io burst time. IO Devices are shown in each one's own column for readability.
        
        PARAMETERS
            None

        RETURNS
            table   : Table
                --returns the created table instance
        """
        table = Table(title="I/O Devices")     #Create table
        size = len(self.io)                    #Get size of the table

        #Upper right rorner Should not have anything in it
        table.add_column('  ', justify='center', no_wrap=True)

        #Add a column for every io device given in the list
        for ios in range(size):
            table.add_column(f"I/O {ios + 1}", justify="center", style="cyan", no_wrap=True)

        ids = []
        bursts = []

        #Get each io's process and burst amount
        for block in self.io:
            if(block is not None):                             #There is a pcb currently being run on the io device
                ids.append(f'{block.getPid()}')
                bursts.append(f'{block.getIOBurst()}')
            else:
                ids.append('-----')                            #No process is currently running on the io device
                bursts.append('-----')

        table.add_row('Process ID', *ids, style = 'orange3')   #First row contains each io's process id
        table.add_row('I/O Burst', *bursts, style='cyan')      #Second row contain's each io's burst amount
        
        return table

    def __rich__(self) -> Panel:

        return Panel(self.build_table())
