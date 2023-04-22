import curses
from app.solitaire import *


def main(screen):
	curses.curs_set(0)
	curses.use_default_colors()
	# default foreground color
	curses.init_pair(1, -1, -1)
	# red
	curses.init_pair(2, curses.COLOR_RED, -1)
	# select color
	curses.init_pair(3, curses.COLOR_YELLOW, -1)
	Solitaire(screen)


if __name__ == "__main__":
	curses.wrapper(main)