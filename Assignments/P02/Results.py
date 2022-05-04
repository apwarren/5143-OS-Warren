from Pcb import pcb
from rich.table import Table
from rich.panel import Panel

class results:
    """   
    NAME
        results - Rich table containing the results of a finished simulation

    DESCRIPTION
        Table builder to create a table displaying all statistics 
        being simultated for the scheduling algorithm at the end.
        Shows the first and last three processes to be terminated in the
        end.
        
    ATTRIBUTES
        head    :   list
            --First three pcbs to finish and get terminated
        tail    :   list
            --Last three pcbs to finish and get terminated
    """
    def __init__(self, f, l):
        self.head = f
        self.tail = l

    def build_table(self):
        """   
        NAME
            build_table - Table created based on end statistics

        DESCRIPTION
            Table builder to create a table displaying all the results of the
            scheduling algorithm. It shows the first and last three pcb's results
            of which includes each one's id, turn around time, cpu wait time, 
            and io wait time. This table is only shown once all processes
            have finished running and been terminated within the simulation.
        
        PARAMETERS
            None

        RETURNS
            table   : Table
                --returns the created table instance
        """
        table = Table(title="Results")  #This table is the results table

        table.add_column("Finished First", justify="center", style="cyan", no_wrap=True)
        table.add_column("Process ID", style="magenta")
        table.add_column("TAT", justify="right", style="green")
        table.add_column("CPU Wait Time", justify="right", style="blue")
        table.add_column("I/O Wait Time", justify="right", style="red")
        table.add_column('    ')
        table.add_column('Finished Last', justify="center", style="cyan", no_wrap=True)
        table.add_column("Process ID", style="magenta")
        table.add_column("TAT", justify="right", style="green")
        table.add_column("CPU Wait Time", justify="right", style="blue")
        table.add_column("I/O Wait Time", justify="right", style="red")

        for first in range(len(self.head)):
            table.add_row(f'First {first + 1}', str(self.head[first].getPid()), str(self.head[first].getTAT()), 
            str(self.head[first].getCPUWait()), str(self.head[first].getIOWait()), 
            '   ', f'Last {first +1}', str(self.tail[first].getPid()), str(self.tail[first].getTAT()), 
            str(self.tail[first].getCPUWait()), str(self.tail[first].getIOWait()))
        
        return table

    def __rich__(self) -> Panel:

        return Panel(self.build_table())
