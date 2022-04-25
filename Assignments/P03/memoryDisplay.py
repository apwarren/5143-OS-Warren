from rich.panel import Panel
from rich.table import Table

class memDisplay():
    def __init__(self, mem):
        memory = mem
        
    def build_table(self):
        table = Table(title="Writing Memory")
        table.add_column('  ', justify='center', no_wrap=True)
        table.add_column(f"A_Memory", justify="center", style="cyan", no_wrap=True)
        table.add_column(f"Value", justify="center", style="cyan", no_wrap=True)
        table.add_column(f"B_Memory", justify="center", style="cyan", no_wrap=True)
        table.add_column(f"Value", justify="center", style="cyan", no_wrap=True)
        table.add_column(f"C_Memory", justify="center", style="cyan", no_wrap=True)
        table.add_column(f"Value", justify="center", style="cyan", no_wrap=True)

        for block, index in self.memory:
            for ind, value in index:
                table.add_row('', ind, value, ind, self.memory['B'][ind], ind, self.memory['C'][ind], style = 'orange3')


    def __rich__(self) -> Panel:

        return Panel(self.build_table())