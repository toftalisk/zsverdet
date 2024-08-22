class MapDrawer:
    def __init__(self, curses, stdscr):
        self.curses = curses
        self.stdscr = stdscr
        self.colorCount = 1
        self.colors = dict()

        # Initialize curses
        curses.curs_set(0)
        stdscr.nodelay(1)
        stdscr.timeout(100)

        # Define colors
        curses.start_color()

        self.define_color(curses.COLOR_GREEN, curses.COLOR_BLACK, "green")
        self.define_color(curses.COLOR_WHITE, curses.COLOR_BLACK, "white")
        self.define_color(curses.COLOR_RED, curses.COLOR_BLACK, "red")
        self.define_color(curses.COLOR_BLUE, curses.COLOR_BLACK, "blue")

    def define_color(self, forground, background, name):
        self.curses.init_pair(self.colorCount, forground, background)
        self.colors[name] = self.colorCount
        self.colorCount = self.colorCount + 1

    def draw_world(self, world):
        self.draw([element for row in world for element in row])

    def draw(self, game_objects):
        for game_object in game_objects:
            color = self.get_color(game_object)
            self.stdscr.addch(game_object.y, game_object.x, game_object.char, self.curses.color_pair(color))

    def get_color(self, game_object):
        if game_object.color in self.colors:
            return self.colors[game_object.color]
        raise SyntaxError("Unknown color " + str(game_object.color) + " type=" + game_object.char)
