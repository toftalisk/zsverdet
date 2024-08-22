import curses

from game_object import GameObject

class MoveableGameObject(GameObject):
    def __init__(self, x, y, char, health):
        super().__init__(x, y, char, curses.color_pair(5))
        self.health = health
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color