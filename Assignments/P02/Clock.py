from datetime import datetime
from rich.text import Text

class Clock:
    """   
    NAME
        Clock - Simulated amount of time the proccess have run within the simulation

    DESCRIPTION
        Displays the current time that the scheduling simulation has run at a given moment.
        Renders the time in the center of the screen.
        
    ATTRIBUTES
        time    :   int
            --current time accumulated by the simulation

    """
    def __init__(self) -> None:
        self.time = 0   #No time has occured at first

    def addTime(self):
        self.time += 1  #One clock tick has occured

    def __rich__(self) -> Text:
        #Show clock display at the top center is a pink color
        return Text(f'Clock: {self.time}', style="bold deep_pink3", justify="center")