from rich.panel import Panel
from rich.table import Table

class onCPU():
    def __init__(self, pid):
        self.id = pid

    def build_table(self):
        table = Table()
        table.add_column('', justify='center', no_wrap=True, style= 'yellow3')
        table.add_column('', justify="center", style="magenta", no_wrap=True)

        table.add_row('ID', f'{self.id}', style = 'orange3')

        return table


    def __rich__(self) -> Panel:

        return Panel(self.build_table(), title=' Current Process on CPU')