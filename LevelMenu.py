from Menu import Menu

class LevelMenu(Menu):
    L1, L2, L3, L4, L5 = 1, 2, 3, 4, 5

    def __init__(self, size):
        Menu.__init__(self, size, 'Choose your difficulty', \
                [{'name': '10x10', 'code': 1}, {'name': '15x10', 'code': 2}, \
                {'name': '20x20', 'code': 3}, {'name': '40x25', 'code': 4}, \
                {'name': '50x30', 'code': 5}])
        self.name = 'level'
