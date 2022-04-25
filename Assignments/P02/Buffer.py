from rich.panel import Panel

class Buffer:
    def __init__(self, sized = 100, Title = 'Buffer', Reversed = False):
        self.size = int(sized)
        self.currentSize = 0
        self.bar = ""
        self.title = Title
        self.colors = ['[green on #00FF00]', '[chartreuse1 on #87FF00]', '[yellow on #FFFF00]', 
        '[dark_orange3 on #FF8700]', '[red on #FF0000]']
        self.color = '[blue on #0000FF]'
        self.reversed = Reversed

    def increase_buffer(self):
        self.currentSize += 1
    
    def decrease_buffer(self):
        self.currentSize -= 1

    def generate_buffer(self):
        self.bar = ""
        fill = int(self.currentSize / self.size * 100)

        for clr in range(len(self.colors)):
            if(fill <= ((clr+1) * 20) and self.reversed is False):
                self.color = self.colors[clr]
                break
            elif(fill <= ((clr+1) * 20) and self.reversed is True):
                self.color = self.colors[-(clr+1)]
                break
            else:
                continue
            
        for i in range(fill):
            self.bar += '  '

        return self.color
        
    def __rich__(self) -> Panel:
        self.generate_buffer()
        return Panel(f'{self.color}{self.bar}', title = self.title)
