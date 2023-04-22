import unittest
from random import choice
from app.gamehandler import *


class TestGameHandler(unittest.TestCase):
	def test_initialization(self):
		game_handler = GameHandler()
		self.assertEqual(game_handler.discard, [])
		for suit in Card.SUITS:
			self.assertEqual(game_handler.ace_piles[suit], [])
		deck_card_count = 52
		for i in range(game_handler.COLUMNS):
			# column has been populated
			self.assertEqual(len(game_handler.columns[i]), i + 1)
			# top card in column is face up
			self.assertTrue(game_handler.columns[i][-1].face_up)
			deck_card_count -= (i + 1)
		self.assertEqual(len(game_handler.deck), deck_card_count)

	def test_draw(self):
		game_handler = GameHandler()
		card1 = get_random_card()
		card2 = get_random_card()
		game_handler.deck = [card1, card2]
		game_handler.discard = []
		game_handler.draw()
		self.assertEqual(game_handler.deck, [card1])
		self.assertEqual(game_handler.discard, [card2])
		self.assertTrue(card2.face_up)

	def test_draw_empty_deck(self):
		game_handler = GameHandler()
		card1 = get_random_card()
		card2 = get_random_card()
		game_handler.deck = []
		game_handler.discard = [card1.flip(), card2.flip()]
		game_handler.draw()
		self.assertEqual(game_handler.deck, [card2])
		self.assertEqual(game_handler.discard, [card1])
		self.assertTrue(card1.face_up)
		self.assertFalse(card2.face_up)

	def test_discard_ace_to_ace_pile(self):
		game_handler = GameHandler()
		ace = Card(1, get_random_suit())
		game_handler.discard = [ace.flip()]
		game_handler.discard_to_ace_pile()
		ace_pile = game_handler.ace_piles[ace.suit]
		self.assertFalse(game_handler.discard)
		self.assertEqual(len(ace_pile), 1)
		self.assertEqual(ace_pile[-1], ace)

	def test_discard_to_ace_pile_empty_discard(self):
		game_handler = GameHandler()
		self.assertRaises(IllegalMoveError, game_handler.discard_to_ace_pile)

	def test_discard_to_ace_pile_valid(self):
		game_handler = GameHandler()
		top_card = Card(choice(range(1, 13)), get_random_suit())
		discard_card = Card(top_card.value + 1, top_card.suit)
		game_handler.ace_piles[top_card.suit] = [top_card.flip()]
		game_handler.discard = [discard_card.flip()]
		game_handler.discard_to_ace_pile()
		self.assertEqual(len(game_handler.ace_piles[top_card.suit]), 2)
		self.assertFalse(game_handler.discard)

	def test_discard_to_empty_ace_pile_invalid(self):
		game_handler = GameHandler()
		not_ace = Card(choice(range(2, 14)), get_random_suit())
		game_handler.discard = [not_ace.flip()]
		self.assertRaises(IllegalMoveError, game_handler.discard_to_ace_pile)
		self.assertFalse(game_handler.ace_piles[not_ace.suit])
		self.assertEqual(len(game_handler.discard), 1)

	def test_discard_to_ace_pile_invalid(self):
		game_handler = GameHandler()
		suit = get_random_suit()
		ace = Card(1, suit)
		invalid_card = Card(choice(range(3, 14)), suit)
		game_handler.ace_piles[suit] = [ace.flip()]
		game_handler.discard = [invalid_card.flip()]
		self.assertRaises(IllegalMoveError, game_handler.discard_to_ace_pile)
		self.assertEqual(len(game_handler.ace_piles[suit]), 1)
		self.assertEqual(len(game_handler.discard), 1)

	def test_discard_king_to_empty_column(self):
		game_handler = GameHandler()
		king = Card(13, get_random_suit())
		game_handler.discard = [king.flip()]
		game_handler.columns[0] = []
		game_handler.discard_to_column(0)
		self.assertFalse(game_handler.discard)
		self.assertEqual(len(game_handler.columns[0]), 1)
		self.assertEqual(game_handler.columns[0][-1], king)

	def test_empty_discard_to_column(self):
		game_handler = GameHandler()
		self.assertRaises(IllegalMoveError, game_handler.discard_to_column, 0)

	def test_discard_to_column_valid(self):
		game_handler = GameHandler()
		top_card = Card(choice(range(2, 14)), choice(["spades", "clubs"]))
		discard_card = Card(top_card.value - 1, choice(["hearts", "diamonds"]))
		game_handler.columns[0] = [top_card.flip()]
		game_handler.discard = [discard_card.flip()]
		game_handler.discard_to_column(0)
		self.assertFalse(game_handler.discard)
		self.assertEqual(len(game_handler.columns[0]), 2)
		self.assertEqual(game_handler.columns[0][-1], discard_card)

	def test_discard_to_column_invalid_value(self):
		game_handler = GameHandler()
		top_card = Card(choice(range(1, 7)), choice(["spades", "clubs"]))
		discard_card = Card(choice(range(7, 14)), choice(["hearts", "diamonds"]))
		game_handler.columns[0] = [top_card.flip()]
		game_handler.discard = [discard_card.flip()]
		self.assertRaises(IllegalMoveError, game_handler.discard_to_column, 0)
		self.assertEqual(game_handler.discard, [discard_card])
		self.assertEqual(game_handler.columns[0], [top_card])

	def test_discard_to_column_invalid_suit(self):
		game_handler = GameHandler()
		top_card = Card(choice(range(2, 14)), choice(["spades", "clubs"]))
		discard_card = Card(top_card.value - 1, choice(["spades", "clubs"]))
		game_handler.columns[0] = [top_card.flip()]
		game_handler.discard = [discard_card.flip()]
		self.assertRaises(IllegalMoveError, game_handler.discard_to_column, 0)
		self.assertEqual(game_handler.discard, [discard_card])
		self.assertEqual(game_handler.columns[0], [top_card])

	def test_column_to_ace_pile_ace(self):
		game_handler = GameHandler()
		ace = Card(1, get_random_suit())
		game_handler.columns[0] = [ace.flip()]
		game_handler.column_to_ace_pile(0)
		ace_pile = game_handler.ace_piles[ace.suit]
		self.assertFalse(game_handler.columns[0])
		self.assertEqual(len(ace_pile), 1)
		self.assertEqual(ace_pile[-1], ace)

	def test_column_to_ace_pile_flips_if_needed(self):
		game_handler = GameHandler()
		ace = Card(1, get_random_suit())
		card = get_random_card()
		game_handler.columns[0] = [card, ace.flip()]
		game_handler.column_to_ace_pile(0)
		ace_pile = game_handler.ace_piles[ace.suit]
		self.assertEqual(len(game_handler.columns[0]), 1)
		self.assertEqual(len(ace_pile), 1)
		self.assertEqual(ace_pile[-1], ace)
		self.assertTrue(game_handler.columns[0][0].face_up)

	def test_column_to_ace_pile_empty_column(self):
		game_handler = GameHandler()
		game_handler.columns[0] = []
		self.assertRaises(IllegalMoveError, game_handler.column_to_ace_pile, 0)

	def test_column_to_ace_pile_valid(self):
		game_handler = GameHandler()
		top_card = Card(choice(range(1, 13)), get_random_suit())
		card = Card(top_card.value + 1, top_card.suit)
		game_handler.ace_piles[top_card.suit] = [top_card.flip()]
		game_handler.columns[0] = [card.flip()]
		game_handler.column_to_ace_pile(0)
		self.assertEqual(len(game_handler.ace_piles[top_card.suit]), 2)
		self.assertFalse(game_handler.columns[0])

	def test_column_to_empty_ace_pile_invalid(self):
		game_handler = GameHandler()
		not_ace = Card(choice(range(2, 14)), get_random_suit())
		game_handler.columns[0] = [not_ace.flip()]
		self.assertRaises(IllegalMoveError, game_handler.column_to_ace_pile, 0)
		self.assertFalse(game_handler.ace_piles[not_ace.suit])
		self.assertEqual(len(game_handler.columns[0]), 1)

	def test_column_to_ace_pile_invalid(self):
		game_handler = GameHandler()
		suit = get_random_suit()
		ace = Card(1, suit)
		invalid_card = Card(choice(range(3, 14)), suit)
		game_handler.ace_piles[suit] = [ace.flip()]
		game_handler.columns[0] = [invalid_card.flip()]
		self.assertRaises(IllegalMoveError, game_handler.column_to_ace_pile, 0)
		self.assertEqual(len(game_handler.ace_piles[suit]), 1)
		self.assertEqual(len(game_handler.columns[0]), 1)

	def test_empty_column_to_column(self):
		game_handler = GameHandler()
		game_handler.columns[0] = []
		self.assertRaises(IllegalMoveError, game_handler.column_to_column, 0, 1)

	def test_column_to_column_single_card(self):
		game_handler = GameHandler()
		king = Card(13, get_random_suit())
		game_handler.columns[0] =[king.flip()]
		game_handler.columns[1] = []
		game_handler.column_to_column(0, 1)
		self.assertFalse(game_handler.columns[0])
		self.assertEqual(game_handler.columns[1], [king])

	def test_column_to_column_flips(self):
		game_handler = GameHandler()
		king = Card(13, get_random_suit())
		card = get_random_card()
		game_handler.columns[0] = [card, king.flip()]
		game_handler.columns[1] = []
		game_handler.column_to_column(0, 1)
		self.assertEqual(game_handler.columns[0], [card])
		self.assertEqual(game_handler.columns[1], [king])
		self.assertTrue(game_handler.columns[0][0].face_up)

	def test_column_to_column_multiple_cards(self):
		game_handler = GameHandler()
		king = Card(13, choice(["spades", "clubs"]))
		queen = Card(12, choice(["hearts", "diamonds"]))
		jack = Card(11, choice(["spades", "clubs"]))
		game_handler.columns[0] = [king.flip(), queen.flip(), jack.flip()]
		game_handler.columns[1] = []
		game_handler.column_to_column(0, 1, 3)
		self.assertFalse(game_handler.columns[0])
		self.assertEqual(game_handler.columns[1], [king, queen, jack])


def get_random_suit():
	return choice(list(Card.SUITS.keys()))

def get_random_card():
	value = choice(Card.VALUES)
	suit = get_random_suit()
	return Card(value, suit)


if __name__ == "__main__":
	unittest.main()