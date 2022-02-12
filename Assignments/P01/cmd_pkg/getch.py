'''
Class   : Getch
    Getch has been provided and written by Dr. Griffin. This function takes input from
    the user and does not print said input to the terminal. Instead it stores it to a given
    char to be used by the programmer. For this shell, the getch is used to obtain input
    from the terminal and then append each character to a string to be sent as the
    command and parameters of the shell. Getching is also used within the Less command
    to allow the user to press specific keys in order to traverse through the given
    file's contents.
'''

class Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): 
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
