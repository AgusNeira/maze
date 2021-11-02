from Menu import Menu

class StartMenu(Menu):
    PLAY, EXIT = 1, 2
    def __init__(self, size):
        Menu.__init__(self, size, 'The Maze', [{'name': 'Play', 'code': 1}, \
            {'name': 'Exit', 'code': 2}])
        self.name = 'start'
