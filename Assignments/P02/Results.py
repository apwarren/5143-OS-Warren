from Pcb import pcb
from rich.table import Table
from rich.panel import Panel

class results:
    """Renders the time in the center of the screen."""

    def __init__(self, f, l):
        self.head = f
        self.tail = l

    def build_table(self):
        table = Table(title="Results")
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
