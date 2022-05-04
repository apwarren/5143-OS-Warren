import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import json

# console = Console()

class memTable():

    """Renders the time in the center of the screen."""

    def __init__(self, memry):
        self.memory = memry

    def build_table(self):
        table = Table(title="Memory")
        df = pd.DataFrame.from_dict(self.memory, orient='index').reset_index(drop=True)
        df = df.transpose()
        df.rename(columns = {0:'A', 1:'B', 2: 'C'}, inplace = True)
        df.index.name = ''
        df.reset_index(inplace=True)
        
        """Convert a pandas.DataFrame obj into a rich.Table obj.
            Args:
                pandas_dataframe (DataFrame): A Pandas DataFrame to be converted to a rich Table.
                rich_table (Table): A rich Table that should be populated by the DataFrame values.
                show_index (bool): Add a column with a row count to the table. Defaults to True.
                index_name (str, optional): The column name to give to the index column. Defaults to None, showing no value.
            Returns:
                Table: The rich Table instance passed, populated with the DataFrame values."""


        for column in df.columns:
            table.add_column(str(column), style= 'cyan')

        for index, value_list in enumerate(df.values.tolist()):
            row = []
            row += [str(x) for x in value_list]
            table.add_row(*row)

        return table

    def __rich__(self) -> Panel:

        return Panel(self.build_table())
   

# if __name__ == '__main__':
#     with open('memory.json') as f:
#         memory = json.load(f)

#     table = memTable(memory)
#     console.print(table)
