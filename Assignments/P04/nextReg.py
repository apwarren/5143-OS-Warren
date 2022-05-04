from rich.panel import Panel
from rich.table import Table

class nextPriv():
    def __init__(self, priv):
        self.privilege = priv

    def build_table(self):
        table = Table()
        table.add_column('', justify='center', no_wrap=True, style= 'yellow3')
        table.add_column('', justify="center", style="medium_violet_red", no_wrap=True)

        table.add_row('#', f'{self.privilege}', style = 'orange3')

        return table


    def __rich__(self) -> Panel:

        return Panel(self.build_table(), title='Next Privileged Instruction')