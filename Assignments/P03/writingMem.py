from rich.panel import Panel
from rich.table import Table

class writeMem():
    def __init__(self, A = 'None', B = 'None', C = 'None'):
        self.A = A
        self.B = B
        self.C = C

    def build_table(self):
        table = Table(title="Writing Memory")
        table.add_column('  ', justify='center', no_wrap=True)
        table.add_column(f"A", justify="center", style="yellow3", no_wrap=True)
        table.add_column(f"B", justify="center", style="yellow3", no_wrap=True)
        table.add_column(f"C", justify="center", style="yellow3", no_wrap=True)


        table.add_row('Writing', self.A, self.B, self.C, style = 'orange3')

        return table

    def __rich__(self) -> Panel:

        return Panel(self.build_table())