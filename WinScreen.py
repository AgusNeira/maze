from Menu import Menu

class WinScreen(Menu):
    REPLAY = 1
    LEVELS = 2
    MAIN = 3
    EXIT = 4

    def __init__(self, size):
        Menu.__init__(self, size, 'Congrats! You Won!', \
                [{'name': 'Replay', 'code': 1}, {'name': 'Choose difficulty', 'code': 2}, \
                {'name': 'Main menu', 'code': 3}, {'name': 'Exit', 'code': 4}])
        self.name = 'win'
