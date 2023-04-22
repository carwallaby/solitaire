from curses import KEY_RESIZE, KEY_UP, KEY_DOWN
from functools import partial
from .uihandler import *


class Solitaire:
	def __init__(self, screen):
		self.screen = screen
		self.game_handler = GameHandler()
		self.game_ui_handler = GameUiHandler(self.screen, self.game_handler)
		self._initialize_key_mapping()
		self.play()

	def play(self):
		self.playing = True
		while self.playing:
			x = self.screen.getch()
			if x in self.KEY_MAPPING:
				self.KEY_MAPPING[x]()

	def select_discard(self):
		if self.game_handler.discard:
			self.game_ui_handler.select_discard()

			destinations = {
				ord("a"): self.game_ui_handler.discard_to_ace_pile,
				ord("0"): partial(self.game_ui_handler.discard_to_column, 0),
				ord("1"): partial(self.game_ui_handler.discard_to_column, 1),
				ord("2"): partial(self.game_ui_handler.discard_to_column, 2),
				ord("3"): partial(self.game_ui_handler.discard_to_column, 3),
				ord("4"): partial(self.game_ui_handler.discard_to_column, 4),
				ord("5"): partial(self.game_ui_handler.discard_to_column, 5),
				ord("6"): partial(self.game_ui_handler.discard_to_column, 6)
			}

			dest = self.screen.getch()
			if dest in destinations:
				destinations[dest]()
			else:
				self.game_ui_handler.populate_discard()

	def select_column(self, column_index, num_cards=1):
		column = self.game_handler.columns[column_index]
		can_select_num = (len(column) >= num_cards and
						  column[-num_cards].face_up)

		if num_cards > 0 and can_select_num:
			self.game_ui_handler.select_column(column_index, num_cards)

			destinations = {
				KEY_UP: partial(self.select_column, column_index, num_cards + 1),
				KEY_DOWN: partial(self.select_column, column_index, num_cards - 1),
				ord("0"): partial(self.game_ui_handler.column_to_column,
								  column_index, 0, num_cards),
				ord("1"): partial(self.game_ui_handler.column_to_column,
								  column_index, 1, num_cards),
				ord("2"): partial(self.game_ui_handler.column_to_column,
								  column_index, 2, num_cards),
				ord("3"): partial(self.game_ui_handler.column_to_column,
								  column_index, 3, num_cards),
				ord("4"): partial(self.game_ui_handler.column_to_column,
								  column_index, 4, num_cards),
				ord("5"): partial(self.game_ui_handler.column_to_column,
								  column_index, 5, num_cards),
				ord("6"): partial(self.game_ui_handler.column_to_column,
								  column_index, 6, num_cards),
				ord("a"): partial(self.game_ui_handler.column_to_ace_pile,
								  column_index)
			}

			dest = self.screen.getch()
			if dest in destinations:
				destinations[dest]()
			else:
				self.game_ui_handler.populate_column(column_index)
		else:
			self.game_ui_handler.populate_column(column_index)

	def confirm_quit(self):
		self.playing = False

	def confirm_new_game(self):
		self.game_handler.new_game()
		self.game_ui_handler.draw_screen()

	def _initialize_key_mapping(self):
		self.KEY_MAPPING = {
			KEY_RESIZE: self.game_ui_handler.calibrate_screen,
			ord("q"): self.confirm_quit,
			ord(" "): self.game_ui_handler.draw,
			ord("d"): self.select_discard,
			ord("0"): partial(self.select_column, 0),
			ord("1"): partial(self.select_column, 1),
			ord("2"): partial(self.select_column, 2),
			ord("3"): partial(self.select_column, 3),
			ord("4"): partial(self.select_column, 4),
			ord("5"): partial(self.select_column, 5),
			ord("6"): partial(self.select_column, 6),
			ord("n"): self.confirm_new_game
		}