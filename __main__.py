import curses
import logging

from enemy import Enemy
from game_engine import GameEngine
from game_object import GameObject
from map_drawer import MapDrawer
from player import Player

# Configure logging to write to a file
logging.basicConfig(
    filename='curses_app.log',  # Log file name
    level=logging.DEBUG,        # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

def load_map(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

def interpet_map(raw_map):
    game_objects = []
    game_map = [list(row) for row in raw_map]
    player = Player(0, 0, 100)

    for y, row in enumerate(raw_map):
        for x, char in enumerate(row):
            if char == '#':
                game_map[y][x] = GameObject(x, y, '#', 'white')
            if char == '.':
                game_map[y][x] = GameObject(x, y, '.', 'white')
            if char == 'z':
                player.x = x
                player.y = y
                game_objects.append(player)
                game_map[y][x] = GameObject(x, y, '.', 'white')
            if char == 'g':
                game_objects.append(Enemy(x, y, 'g', 'blue', 100))
                game_map[y][x] = GameObject(x, y, '.', 'white')
            elif char == '=':
                game_map[y][x] = GameObject(x, y, '=', 'red')
            elif char in '<>':
                game_map[y][x] = GameObject(x, y, char, 'white')

    return (player, game_objects, game_map)


def draw_health_bar(stdscr, health):
    health_str = f"Health: {health}/100"
    stdscr.addstr(0, 0, health_str, curses.color_pair(2))

def main(stdscr):

    raw_map = load_map('game_map_z.txt')
    (player, game_objects, game_map) = interpet_map(raw_map)
    game_engine = GameEngine(game_objects, game_map, player)
    map_drawer = MapDrawer(curses, stdscr)

    init_world = game_engine.get_current_map()
    map_drawer.draw_world(init_world)

    while True:
        key = stdscr.getch()
        player.handle_input(key, game_map)

        updates = game_engine.update()
        logging.info(list(map(lambda u: f"({u.x}, {u.y})", updates)))

        draw_health_bar(stdscr, player.health)

        map_drawer.draw(updates)

        stdscr.refresh()

        if game_map[player.y][player.x] == '<':
            current_map_file = 'game_map_z_2.txt'
            game_map = load_map(current_map_file)
            stdscr.clear()  # Clear the screen and redraw the new map
            break

curses.wrapper(main)
