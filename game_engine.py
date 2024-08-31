import copy
import logging

class GameEngine:
    def __init__(self, game_objects, game_map, player):
        self.game_objects = game_objects
        self.game_map = game_map
        self.player = player

    def update(self, key):
        updates = []
        for game_object in self.game_objects:
            (oldX,oldY) = (game_object.x, game_object.y)
            game_object.update(self.game_map, self.player)
            (newX,newY) = (game_object.x, game_object.y)
            new_map = self.get_current_map()
            if oldX != newX or oldY != newY:
                updates.append(new_map[oldY][oldX])
                updates.append(new_map[newY][newX])

        player_moved, oldX, oldY = self.player.handle_input(key, self.game_map)
        if player_moved:
            logging.info(str(oldX) + ", " + str(oldY) + " new: " + str(self.player.x) + ", " + str(self.player.y))
            new_map = self.get_current_map()
            updates.append(new_map[oldY][oldX])
            updates.append(new_map[self.player.y][self.player.x])

        return updates

    def get_current_map(self):
        new_map = copy.deepcopy(self.game_map.copy())
        for game_object in self.game_objects:
            new_map[game_object.y][game_object.x] = game_object
        return new_map
