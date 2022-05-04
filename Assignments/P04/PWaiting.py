from rich.panel import Panel
from rich.table import Table

class PWaitTable():
    def __init__(self, waiters = []):
        self.waiting = waiters

    def build_table(self):
        table = Table()
        ids = []
        if(self.waiting == []):
            ids.append('---')
            
        table.add_column('', justify='center', no_wrap=True, style = 'yellow3')
        for waiter in self.waiting:
            table.add_column('', justify='center', no_wrap=True)
            ids.append(f'P{waiter.getPid()}')


        table.add_row('ID', *ids, style = 'orange3')

        return table


    def __rich__(self) -> Panel:

        return Panel(self.build_table(), title= 'Waiting For Privileged Access')