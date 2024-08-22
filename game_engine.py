import logging

class GameEngine:
    def __init__(self, game_objects, game_map, player):
        self.game_objects = game_objects
        self.game_map = game_map
        self.player = player

    def update(self):
        current = self.get_current_map()
        updates = []
        for game_object in self.game_objects:
            (oldX,oldY) = (game_object.x, game_object.y)
            game_object.update(self.game_map, self.player)
            (newX,newY) = (game_object.x, game_object.y)
            if oldX != newX or oldY != newY:
                updates.append(current[oldY][oldX])
                updates.append(current[newY][newX])

        return updates

    def get_current_map(self):
        new_map = self.game_map.copy()
        for game_object in self.game_objects:
            new_map[game_object.y][game_object.x] = game_object
        return new_map
