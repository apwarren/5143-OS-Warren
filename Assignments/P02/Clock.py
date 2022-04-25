from datetime import datetime
from rich.text import Text

class Clock:
    """Renders the time in the center of the screen."""
    def __init__(self) -> None:
        self.time = 0

    def addTime(self):
        self.time += 1

    def __rich__(self) -> Text:
        return Text(f'Clock: {self.time}', style="bold deep_pink3", justify="center")