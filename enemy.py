from moveable_game_object import MoveableGameObject
from util import roll

class Enemy(MoveableGameObject):
    def __init__(self, x, y, char, color, max_health, speed):
        super().__init__(x, y, char, color)
        self.health = max_health
        self.cooldown = 1000 - speed
        self.cooldownLeft = self.cooldown

    def update(self, game_map, player):
        self.cooldownLeft = self.cooldownLeft - 1
        if (self.cooldownLeft == 0):
            self.cooldownLeft = self.cooldown
            self.move(game_map, player)

    def move (self, game_map, player):
        if self.x < player.x:
            self.x += 1
        elif self.x > player.x:
            self.x -= 1
        if self.y < player.y:
            self.y += 1
        elif self.y > player.y:
            self.y -= 1

        # Check if the enemy is on the player position and attack
        if self.x == player.x and self.y == player.y:
            damage = roll(4, 4)
            player.health -= damage