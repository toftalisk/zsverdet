import curses
import random

def load_map(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

def roll(n, eyes):
    return sum(random.randint(1, eyes) for _ in range(n))

def draw_health_bar(stdscr, health):
    health_str = f"Health: {health}/100"
    stdscr.addstr(0, 0, health_str, curses.color_pair(6))

def move_guard(guard_x, guard_y, zorro_x, zorro_y, game_map):
    new_x, new_y = guard_x, guard_y
    if guard_x < zorro_x:
        new_x += 1
    elif guard_x > zorro_x:
        new_x -= 1
    if guard_y < zorro_y:
        new_y += 1
    elif guard_y > zorro_y:
        new_y -= 1

    if game_map[new_y][new_x] != '#':
        guard_x, guard_y = new_x, new_y

    return guard_x, guard_y

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Define colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Grass
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Ground
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)  # House walls
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Zorro
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)    # Health bar
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)   # Guards
    curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLACK)   # Guards

    # Define the initial health of Zorro
    health = 100
    zorro_x = 5
    zorro_y = 5

    # Define the map
    game_map = load_map('game_map_z.txt')

    # Counter to slow down guard movement
    guard_move_counter = 0
    guard_move_interval = 5  # Guards move every 5 iterations
    guards = []

    # Create initial positions for guards and zorro
    for y, row in enumerate(game_map):
        for x, char in enumerate(row):
            if (char == 'g'):
                guards.append((x, y))
            elif (char == 'z'):
                zorro_x = x
                zorro_y = y

    while True:
        # Clear the screen
        stdscr.clear()

        # Draw the map
        for y, row in enumerate(game_map):
            for x, char in enumerate(row):
                if char == '#':
                    stdscr.addch(y, x, char, curses.color_pair(4))
                elif char == '.':
                    stdscr.addch(y, x, char, curses.color_pair(3))
                elif char == ' ':
                    stdscr.addch(y, x, char, curses.color_pair(2))
                elif char == '=':
                    stdscr.addch(y, x, char, curses.color_pair(8))

        # Draw Zorro
        stdscr.addch(zorro_y, zorro_x, 'Z', curses.color_pair(5))


        # Draw the health bar
        draw_health_bar(stdscr, health)

        # Move guards when we reach counter
        if guard_move_counter % guard_move_interval == 0:
            new_guards = []
            for (guard_x, guard_y) in guards:
                guard_x, guard_y = move_guard(guard_x, guard_y, zorro_x, zorro_y, game_map)
                new_guards.append((guard_x, guard_y))
            guards = new_guards

        # draw guards
        for (guard_x, guard_y) in guards:
            stdscr.addch(guard_y + 1, guard_x, 'g', curses.color_pair(7))

        # Increment guard move counter
        guard_move_counter += 1

        # Refresh the screen
        stdscr.refresh()

        # Get user input
        key = stdscr.getch()

        # Update Zorro's position based on the user input
        if key == curses.KEY_UP and zorro_y > 0:
            zorro_y -= 1
        elif key == curses.KEY_DOWN and zorro_y < len(game_map) - 1:
            zorro_y += 1
        elif key == curses.KEY_LEFT and zorro_x > 0:
            zorro_x -= 1
        elif key == curses.KEY_RIGHT and zorro_x < len(game_map[0]) - 1:
            zorro_x += 1

        # Prevent Zorro from walking through walls
        if game_map[zorro_y][zorro_x] == '#':
            if key == curses.KEY_UP:
                zorro_y += 1
            elif key == curses.KEY_DOWN:
                zorro_y -= 1
            elif key == curses.KEY_LEFT:
                zorro_x += 1
            elif key == curses.KEY_RIGHT:
                zorro_x -= 1

        # Check if Zorro steps on lava and take damage
        if game_map[zorro_y][zorro_x] == '=':
            damage = roll(1, 10)
            health -= damage
            if health <= 0:
                stdscr.addstr(1, 0, "Zorro has been defeated!", curses.color_pair(6))
                stdscr.refresh()
                stdscr.getch()
                return

        # Guards attack Zorro if they are in the same position
        for (guard_x, guard_y) in guards:
            if guard_x == zorro_x and guard_y == zorro_y:
                damage = roll(4, 4)
                health -= damage
                if health <= 0:
                    stdscr.addstr(1, 0, "Zorro has been defeated!", curses.color_pair(6))
                    stdscr.refresh()
                    stdscr.getch()
                    return



curses.wrapper(main)
