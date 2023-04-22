from .card import *


class GameHandler:
	COLUMNS = 7

	def __init__(self):
		self.new_game()

	def new_game(self):
		self.deck = get_deck()
		self.discard = []
		self.ace_piles = {suit: [] for suit in Card.SUITS}
		self.columns = []
		for i in range(self.COLUMNS):
			column = []
			count = 0
			while count < i:
				column.append(self.deck.pop())
				count += 1
			column.append(self.deck.pop().flip())
			self.columns.append(column)

	def draw(self):
		if not self.deck:
			self.deck = [card.flip() for card in self.discard[::-1]]
			self.discard = []
		self.discard.append(self.deck.pop().flip())

	def discard_to_ace_pile(self):
		self._to_ace_pile(self.discard)

	def discard_to_column(self, column_index):
		if not self.discard:
			raise IllegalMoveError
		card = self.discard[-1]
		column = self.columns[column_index]
		if not self._can_add_to_column(card, column):
			raise IllegalMoveError
		column.append(self.discard.pop())

	def column_to_ace_pile(self, column_index):
		column = self.columns[column_index]
		self._to_ace_pile(column)
		if column and not column[-1].face_up:
			column[-1].flip()

	def column_to_column(self, start_index, end_index, num_cards=1):
		column_snapshot = self.columns[start_index]
		if not column_snapshot:
			raise IllegalMoveError
		card_slice = column_snapshot[-num_cards:]
		end_column = self.columns[end_index]
		if not self._can_add_to_column(card_slice[0], end_column):
			raise IllegalMoveError
		self.columns[start_index] = column_snapshot[:-num_cards]
		for card in card_slice:
			end_column.append(card)
		start_column = self.columns[start_index]
		if start_column and not start_column[-1].face_up:
			start_column[-1].flip()

	def _to_ace_pile(self, origin_list):
		if not origin_list:
			raise IllegalMoveError
		card = origin_list[-1]
		ace_pile = self.ace_piles[card.suit]
		if not self._can_add_to_ace_pile(card, ace_pile):
			raise IllegalMoveError
		ace_pile.append(origin_list.pop())

	# --- validators ---

	def _can_add_to_ace_pile(self, card, ace_pile):
		if not ace_pile:
			# ace can be added to empty pile
			return card.value == 1
		top_card = ace_pile[-1]
		return card.value == top_card.value + 1

	def _can_add_to_column(self, card, column):
		if not column:
			# king can be added to empty column
			return card.value == 13
		top_card = column[-1]
		correct_color = card.is_red != top_card.is_red
		correct_value = card.value == top_card.value - 1
		return correct_value and correct_color


class IllegalMoveError(Exception):
	pass