from Pcb import pcb
from rich.table import Table
from rich.panel import Panel

class Cpu:
    """Renders the time in the center of the screen."""

    def __init__(self, cpus):
        self.cpu = cpus

    def build_table(self):
        table = Table(title="CPUs")
        size = len(self.cpu)
        table.add_column('  ', justify='center', no_wrap=True)
        for cpus in range(size):
            table.add_column(f"CPU {cpus + 1}", justify="center", style="cyan", no_wrap=True)
        # table.add_column("Process ID", style="magenta")
        # table.add_column("Burst", justify="right", style="green")

        ids = []
        bursts = []

        for block in self.cpu:
            if(block is not None):
                ids.append(f'{block.getPid()}')
                bursts.append(f'{block.getCPUBurst()}')
            else:
                ids.append('-----')
                bursts.append('-----')

        table.add_row('Process ID', *ids, style='orange3')
        table.add_row('CPU Burst', *bursts, style='yellow3')
        
        
        return table

    def __rich__(self) -> Panel:

        return Panel(self.build_table())
