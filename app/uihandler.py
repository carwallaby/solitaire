from curses import color_pair
from .gamehandler import *


class GameUiHandler:
	COLUMNS = GameHandler.COLUMNS
	PADDING = 1
	SPACING = 2

	def __init__(self, screen, game_handler):
		self.screen = screen
		self.game_handler = game_handler
		self._screens_initialized = False
		self._min_height = self._min_height()
		self._min_width = self._min_width()
		self._fg = color_pair(1)
		self._red_fg = color_pair(2)
		self._select_fg = color_pair(3)
		self.calibrate_screen()

	def calibrate_screen(self):
		self.height, self.width = self.screen.getmaxyx()
		if self.height < self._min_height or self.width < self._min_width:
			self.please_make_terminal_bigger()
		elif not self._screens_initialized:
			self._initialize_screens()
		else:
			self.draw_screen()

	def draw_screen(self):
		self.screen.clear()
		self.populate_ace_piles()
		self.populate_deck()
		self.populate_discard()
		self.populate_columns()
		self.screen.refresh()

	def draw(self):
		self.game_handler.draw()
		self.populate_deck()
		self.populate_discard()

	def populate_deck(self):
		self.deck.clear()
		deck = self.game_handler.deck
		if not deck:
			self._draw_empty(self.deck)
		else:
			self.deck.box()
			for i in range(Card.HEIGHT - 2):
				self.deck.addstr(i + 1, 1, ("/" * (Card.WIDTH - 2)))
		self.deck.refresh()

	def populate_discard(self):
		self.discard.clear()
		discard = self.game_handler.discard
		if not discard:
			self._draw_empty(self.discard)
		else:
			self._draw_flat_card(self.discard, discard[-1])
		self.discard.refresh()

	def populate_ace_piles(self):
		for suit in Card.SUITS:
			self.populate_ace_pile(suit)

	def populate_ace_pile(self, suit):
		window = self.ace_piles[suit]
		window.clear()
		ace_pile = self.game_handler.ace_piles[suit]
		if not ace_pile:
			self._draw_empty(window)
		else:
			self._draw_flat_card(window, ace_pile[-1])
		window.refresh()

	def populate_columns(self):
		for idx in range(self.COLUMNS):
			self.populate_column(idx)

	def populate_column(self, column_index):
		window = self.columns[column_index]
		window.clear()
		column = self.game_handler.columns[column_index]
		if not column:
			window.addstr(0, 0, Card.TL_CORNER)
			window.addstr(0, Card.WIDTH - 1, Card.TR_CORNER)
			window.addstr(Card.HEIGHT - 1, 0, Card.BL_CORNER)
			window.addstr(Card.HEIGHT - 1,
						  Card.WIDTH - 1,
						  Card.BR_CORNER)
		else:
			top_border = (Card.TL_CORNER +
						  (Card.H_LINE * (Card.WIDTH - 2)) +
						  Card.TR_CORNER)
			bottom_border = (Card.BL_CORNER +
							 (Card.H_LINE * (Card.WIDTH - 2)) +
							 Card.BR_CORNER)
			running_y = 0
			top_card = column[-1]
			card_bottom_display = top_card.display_value + top_card.suit_symbol
			bottom_attr = self._red_fg if top_card.is_red else self._fg

			for card in column:
				window.addstr(running_y, 0, top_border)
				running_y += 1
				if card.face_up:
					self._draw_line_borders(window, running_y)
					card_top_display = card.suit_symbol + card.display_value
					attr = self._red_fg if card.is_red else self._fg
					window.addstr(running_y, 1, card_top_display, attr)
					running_y += 1
			for i in range(Card.HEIGHT - 4):
				self._draw_line_borders(window, running_y)
				running_y += 1
			self._draw_line_borders(window, running_y)
			window.addstr(running_y,
						  Card.WIDTH - len(card_bottom_display) - 1,
						  card_bottom_display,
						  bottom_attr)
			window.addstr(running_y + 1, 0, bottom_border)
		window.refresh()

	def select_discard(self):
		self.discard.clear()
		discard = self.game_handler.discard
		self._draw_flat_card(self.discard, discard[-1], self._select_fg)
		self.discard.refresh()

	def select_column(self, column_index, num_cards=1):
		window = self.columns[column_index]
		column = self.game_handler.columns[column_index]
		column_height = 0
		for card in column:
			if card.face_up:
				column_height += 2
			else:
				column_height += 1
		column_height += (Card.HEIGHT - 2)
		top_border = (Card.TL_CORNER +
					  (Card.H_LINE * (Card.WIDTH - 2)) +
					  Card.TR_CORNER)
		bottom_border = (Card.BL_CORNER +
						 (Card.H_LINE * (Card.WIDTH - 2)) +
						 Card.BR_CORNER)
		attr = self._select_fg
		running_y = column_height - 1
		# bottom border
		window.addstr(running_y, 0, bottom_border, attr)
		running_y -= 1
		# select bottom card
		for _ in range(Card.HEIGHT - 2):
			self._draw_line_borders(window, running_y, attr)
			running_y -= 1
		# select additional cards
		for _ in range(1, num_cards):
			self._draw_line_borders(window, running_y, attr)
			self._draw_line_borders(window, running_y - 1, attr)
			running_y -= 2
		window.addstr(running_y, 0, top_border, attr)
		window.refresh()

	def column_to_column(self, start_index, end_index, num_cards):
		try:
			self.game_handler.column_to_column(start_index,
											   end_index,
											   num_cards)
			self.populate_columns()
		except IllegalMoveError:
			self.populate_columns()

	def column_to_ace_pile(self, column_index):
		try:
			self.game_handler.column_to_ace_pile(column_index)
			self.populate_columns()
			self.populate_ace_piles()
		except IllegalMoveError:
			self.populate_columns()

	def discard_to_ace_pile(self):
		try:
			self.game_handler.discard_to_ace_pile()
			self.populate_discard()
			self.populate_ace_piles()
		except IllegalMoveError:
			self.populate_discard()

	def discard_to_column(self, column_index):
		try:
			self.game_handler.discard_to_column(column_index)
			self.populate_discard()
			self.populate_column(column_index)
		except IllegalMoveError:
			self.populate_discard()

	def please_make_terminal_bigger(self):
		msg = "please make your terminal larger :) i am tall!"
		start_x = (self.width - len(msg)) // 2
		start_y = self.height // 2
		self.screen.clear()
		self.screen.addstr(start_y, start_x, msg)
		self.screen.refresh()

	def _initialize_screens(self):
		# initialize ace pile windows
		self.ace_piles = {}
		for i, suit in enumerate(Card.SUITS):
			start_y = self.PADDING
			start_x = (i * Card.WIDTH) + (i * self.SPACING) + self.PADDING
			ace_pile = self.screen.subwin(Card.HEIGHT,
										  Card.WIDTH,
										  start_y,
										  start_x)
			self.ace_piles[suit] = ace_pile

		# initialize deck
		deck_start_y = self.PADDING
		# calculate starting x
		deck_start_x = self._min_width
		deck_start_x -= self.PADDING
		deck_start_x -= (Card.WIDTH * 2)
		deck_start_x -= self.SPACING
		self.deck = self.screen.subwin(Card.HEIGHT,
									   Card.WIDTH,
									   deck_start_y,
									   deck_start_x)

		# initialize discard
		discard_start_y = self.PADDING
		discard_start_x = deck_start_x + self.SPACING + Card.WIDTH
		self.discard = self.screen.subwin(Card.HEIGHT,
										  Card.WIDTH,
										  discard_start_y,
										  discard_start_x)

		# initialize columns
		self.columns = []
		max_column_height = self._max_column_height()
		column_start_y = Card.HEIGHT + self.PADDING + self.SPACING
		for i in range(self.COLUMNS):
			start_x = self.PADDING + (i * Card.WIDTH) + (i * self.SPACING)
			column = self.screen.subwin(max_column_height,
										Card.WIDTH,
										column_start_y,
										start_x)
			self.columns.append(column)

		self._screens_initialized = True
		self.draw_screen()

	def _draw_empty(self, window):
		window.border(" ", " ", " ", " ", 0, 0, 0, 0)

	def _draw_flat_card(self, window, card, attr=None):
		attr = attr if attr else self._fg
		window.attron(attr)
		window.box()
		window.attroff(attr)
		card_top_display = card.suit_symbol + card.display_value
		card_bottom_display = card.display_value + card.suit_symbol
		color = self._red_fg if card.is_red else self._fg
		window.addstr(1, 1, card_top_display, color)
		window.addstr(Card.HEIGHT - 2,
					  Card.WIDTH - len(card_bottom_display) - 1,
					  card_bottom_display,
					  color)

	def _draw_line_borders(self, window, y, attr=None):
		attr = attr if attr else self._fg
		window.addstr(y, 0, Card.V_LINE, attr)
		window.addstr(y, Card.WIDTH - 1, Card.V_LINE, attr)

	def _min_width(self):
		width = Card.WIDTH * self.COLUMNS
		# add padding on either side
		width += (self.PADDING * 2)
		# add spacing between columns
		width += (self.SPACING * (self.COLUMNS - 1))
		return width

	def _min_height(self):
		height = self._max_column_height()
		# top row with ace piles and deck/discard
		height += Card.HEIGHT
		# add spacing and padding
		height += self.SPACING
		height += (self.PADDING * 2)
		return height

	def _max_column_height(self):
		max_face_down = self.COLUMNS - 1
		max_face_up_covered = max(Card.VALUES) - 1
		# 1 row for each face-down card
		height = max_face_down
		# 2 rows for each face-up covered card
		height += (max_face_up_covered * 2)
		height += Card.HEIGHT
		return height