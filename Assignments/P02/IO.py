from Pcb import pcb
from rich.table import Table
from rich.panel import Panel

class IO:
    """Renders the time in the center of the screen."""

    def __init__(self, ios):
        self.io = ios
    
    def build_table(self):
        table = Table(title="I/O Devices")
        size = len(self.io)
        table.add_column('  ', justify='center', no_wrap=True)

        for ios in range(size):
            table.add_column(f"I/O {ios + 1}", justify="center", style="cyan", no_wrap=True)

        ids = []
        bursts = []

        for block in self.io:
            if(block is not None):
                ids.append(f'{block.getPid()}')
                bursts.append(f'{block.getIOBurst()}')
            else:
                ids.append('-----')
                bursts.append('-----')

        table.add_row('Process ID', *ids, style = 'orange3')
        table.add_row('I/O Burst', *bursts, style='cyan')
        
        
        return table

    def __rich__(self) -> Panel:

        return Panel(self.build_table())
