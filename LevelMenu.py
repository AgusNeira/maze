from Menu import Menu

class LevelMenu(Menu):
    L1, L2, L3, L4, L5, L6 = 1, 2, 3, 4, 5, 6

    def __init__(self, size):
        Menu.__init__(self, size, 'Choose your difficulty', \
                [{'name': '10x10', 'code': 1}, {'name': '15x10', 'code': 2}, \
                {'name': '20x20', 'code': 3}, {'name': '30x25', 'code': 4}, \
                {'name': '40x25', 'code': 5}, {'name': '50x30', 'code': 6}])
        self.name = 'level'
