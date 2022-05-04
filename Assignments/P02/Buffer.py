from rich.panel import Panel

class Buffer:
    """   
    NAME
        Buffer - Rich bar showing a queue's currently status as a buffer

    DESCRIPTION
        Creates a buffer or bar showing a colored indicator of how
        far along a queue is within the system or how full the queue is.
        The buffer can shrink and grow when desired. Size is determined based
        on percentage of fullness the buffer can potentially get.
        
    ATTRIBUTES
        sized    :   int
            --Max size amount buffer can get. Default is 100

        currentSize :   int
            --Size amount the buffer currenlty holds

        Title   :   string
            --Name of the given buffer to display. Default is called Buffer

        Reversed    :   bool
            --Whether color indicator order of buffer should be reversed. Used for Terminated Queue Only

        bar :   string
            --Bar for displaying buffer 'image'

        colors  :   list
            --list of colors in order to show based on queue size at a given moment

        color   :   string
            --color currently being displayed on buffer. Default is blue for testing purposes.
    """
    def __init__(self, sized = 100, Title = 'Buffer', Reversed = False):
        self.size = int(sized)  #Max Buffer Size
        self.currentSize = 0    #Current Buffer Size
        self.bar = ""           #Buffer is initially empty
        self.title = Title      #Name of given buffer

        #Color order that buffer goes through based on currentSize
        self.colors = ['[green on #00FF00]', '[chartreuse1 on #87FF00]', '[yellow on #FFFF00]', 
        '[dark_orange3 on #FF8700]', '[red on #FF0000]']

        #Current Color being shown on the buffer
        self.color = '[blue on #0000FF]'

        #Reverse colors order if needed. Used for terminated Queue
        self.reversed = Reversed

    def increase_buffer(self):
        """   
        NAME
            increase_buffer - increments the current size of the buffer

        DESCRIPTION
            increased size of the buffer by 1
            
        PARAMETERS
            NOne

        RETURNS
            None
        """
        self.currentSize += 1
    
    def decrease_buffer(self):
        """   
        NAME
            decrease_buffer - decrements the current size of the buffer

        DESCRIPTION
            decreases size of the buffer by 1
            
        PARAMETERS
            NOne

        RETURNS
            None
        """
        self.currentSize -= 1

    def generate_buffer(self):
        """   
        NAME
            generate_buffer - create instance of the buffer.

        DESCRIPTION
            Creates an instance of the buffer based on the buffer's current size.
            Unless reversed, the buffer will appear green when its size is small
            and will slowly change to red as it gets fuller. For reversed, the opposite
            will be true in which it will initially be red and move toward being green.
            The buffer queue is able to grow and shrink when needed to depict the status
            of the given queue when needed.
            
        PARAMETERS
            NOne

        RETURNS
            None
        """
        self.bar = ""                                   #Start with an empty bar

        fill = int(self.currentSize / self.size * 100)  #Fill the bar based on percentage of how full the queue is

        for clr in range(len(self.colors)):             #Get the right color for bar to be

            if(fill <= ((clr+1) * 20) and self.reversed is False):  #Colors go from green to red
                self.color = self.colors[clr]
                break

            elif(fill <= ((clr+1) * 20) and self.reversed is True): #Colors go from red to green
                self.color = self.colors[-(clr+1)]
                break

            else:
                continue
            
        #Add a space to the bar for each amount of fullness within the buffer
        for i in range(fill):
            self.bar += '  '

        return self.color
        
    def __rich__(self) -> Panel:

        self.generate_buffer()
        #Displaiy created buffer with correct color and size
        return Panel(f'{self.color}{self.bar}', title = self.title)
