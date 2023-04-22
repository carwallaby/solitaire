from random import shuffle


class Card:
	WIDTH = 9
	HEIGHT = 6

	TL_CORNER = "\N{BOX DRAWINGS LIGHT DOWN AND RIGHT}"
	TR_CORNER = "\N{BOX DRAWINGS LIGHT DOWN AND LEFT}"
	BL_CORNER = "\N{BOX DRAWINGS LIGHT UP AND RIGHT}"
	BR_CORNER = "\N{BOX DRAWINGS LIGHT UP AND LEFT}"
	H_LINE = "\N{BOX DRAWINGS LIGHT HORIZONTAL}"
	V_LINE = "\N{BOX DRAWINGS LIGHT VERTICAL}"

	VALUES = range(1, 14)

	SUITS = {
		"clubs": {
			"symbol": "\N{BLACK CLUB SUIT}",
			"is_red": False
		},
		"diamonds": {
			"symbol": "\N{BLACK DIAMOND SUIT}",
			"is_red": True
		},
		"hearts": {
			"symbol": "\N{BLACK HEART SUIT}",
			"is_red": True
		},
		"spades": {
			"symbol": "\N{BLACK SPADE SUIT}",
			"is_red": False
		}
	}

	DISPLAY_VALUES = {
		1: "A",
		11: "J",
		12: "Q",
		13: "K"
	}

	def __init__(self, value, suit):
		# initializes a face-down playing card
		self.value = value
		self.suit = suit
		self.suit_symbol = self.SUITS.get(suit).get("symbol")
		self.display_value = self.DISPLAY_VALUES.get(value, str(value))
		self.is_red = self.SUITS.get(suit).get("is_red")
		self.face_up = False

	def flip(self):
		self.face_up = not self.face_up
		return self

	def __eq__(self, other):
		return self.value == other.value and self.suit == other.suit


def get_deck():
	deck = []
	for suit in Card.SUITS:
		for value in Card.VALUES:
			deck.append(Card(value, suit))
	shuffle(deck)
	return deck