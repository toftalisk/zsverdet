import curses
from moveable_game_object import MoveableGameObject
from util import roll


class Player(MoveableGameObject):
    def __init__(self, x, y, health):
        super().__init__(x, y, 'Z', "white")
        self.health = health

    def handle_input(self, key, game_map):
        old_x, old_y = self.x, self.y

        if key == curses.KEY_UP and self.y > 0:
            self.y -= 1
        elif key == curses.KEY_DOWN and self.y < len(game_map) - 1:
            self.y += 1
        elif key == curses.KEY_LEFT and self.x > 0:
            self.x -= 1
        elif key == curses.KEY_RIGHT and self.x < len(game_map[0]) - 1:
            self.x += 1

        # Prevent walking through walls
        if game_map[self.y][self.x].char == '#':
            if key == curses.KEY_UP:
                self.y += 1
            elif key == curses.KEY_DOWN:
                self.y -= 1
            elif key == curses.KEY_LEFT:
                self.x += 1
            elif key == curses.KEY_RIGHT:
                self.x -= 1

        return (old_x != self.x or old_y != self.y), old_x, old_y


    def update(self, game_map, player):
        # Handle lava damage
        if game_map[self.y][self.x] == '=':
            damage = roll(1, 10)
            self.health -= damage