from rich.panel import Panel
from rich.table import Table

class readMem():
    def __init__(self, A = [], B = [], C = []):
        self.A = A
        self.B = B
        self.C = C
        self.size = max(len(self.A), len(self.B), len(self.C))

    def build_table(self):
        table = Table(title="Reading Memory")
        table.add_column('Reading', justify='center', no_wrap=True)
        table.add_column(f"A", justify="center", style="red3", no_wrap=True)
        table.add_column(f"B", justify="center", style="red3", no_wrap=True)
        table.add_column(f"C", justify="center", style="red3", no_wrap=True)

        if(self.size < 1):
            table.add_row('', '', '',)

        

        for item in range(self.size):
            row = []
            if(item < len(self.A)):
                row.append(str(self.A[item]))
            else:
                row.append('')

            if(item < len(self.B)):
                row.append(str(self.B[item]))
            else:
                row.append('')

            if(item < len(self.C)):
                row.append(str(self.C[item]))
            else:
                row.append('')

            table.add_row('', *row, style = 'orange3')

        return table


    def __rich__(self) -> Panel:

        return Panel(self.build_table())