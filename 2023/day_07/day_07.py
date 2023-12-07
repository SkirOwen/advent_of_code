from __future__ import annotations


from collections import Counter
from functools import cmp_to_key, partial


def parse_lines(lines: list[str]) -> list[tuple[str, int]]:
	parsed = []
	for line in lines:
		card, bid = line.split()
		parsed.append((card, int(bid)))
	return parsed


def get_best_card(card_occ: dict) -> str:
	card_val = "AKQT98765432J"
	max_val = max(card_occ.values())
	for card in card_val:
		if card in card_occ:
			if card_occ[card] == max_val:
				return card


def get_hand(card: str, joker: bool) -> int:
	"""
	This will return a number for odering, so it is easier 
	to know which is hand is better than another.
	"""
	card_occ = dict(Counter(card))		# Occurence, same as np.unique but in a dict

	if joker and "J" in card_occ:
		j = card_occ["J"]
		if len(card_occ) != 1:
			card_occ.pop("J", None)
			best_card = get_best_card(card_occ)
			card_occ[best_card] += j
	else:
		j = 0

	if list(card_occ.values()).count(5) == 1:					
		# Five of a kind
		hand = 7

	elif list(card_occ.values()).count(4) == 1:
		# Four of a kind
		hand = 6

	elif list(card_occ.values()).count(3) == 1 and list(card_occ.values()).count(2) == 1:	
		# Full house
		hand = 5

	elif list(card_occ.values()).count(3) >= 1:	
		# Three of a kind
		hand = 4				

	elif list(card_occ.values()).count(2) == 2:	
		# Two pair
		hand = 3				

	elif list(card_occ.values()).count(2) >= 1:					
		# One pair
		hand = 2

	elif len(card_occ) == 5:					
		# High card
		hand = 1

	return hand
	

def card2nbr(c: str, joker: bool) -> int:
	match c:
		case "A":
			return 14
		case "K":
			return 13
		case "Q":
			return 12
		case "J":
			if joker:
				return 1
			else:
				return 11
		case "T":
			return 10
		case _:
			return int(c)


def compare_cards(card_1: str, card_2: str, joker: bool = False) -> int:
	hand_type_1 = get_hand(card_1, joker=joker)
	hand_type_2 = get_hand(card_2, joker=joker)

	c = 0
	while hand_type_1 == hand_type_2:
		hand_type_1 = card2nbr(card_1[c], joker=joker)
		hand_type_2 = card2nbr(card_2[c], joker=joker)

		c += 1
		if c >= 5:
			break
	
	return hand_type_1 - hand_type_2


def get_card_rank(card_bid, joker: bool = False):

	cards = [c[0] for c in card_bid]

	card_sorted = sorted(
		card_bid,
		key=lambda pair: cmp_to_key(
			partial(compare_cards, joker=joker)
			)(pair[0])
		)
	return card_sorted


def get_total_winnings(card_sorted):
	total = 0
	for i, (card, bid) in enumerate(card_sorted, start=1):
		total += i * bid
	return total


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	card_bid = parse_lines(lines)

	card_sorted = get_card_rank(card_bid)
	total_winnings = get_total_winnings(card_sorted)
	print(f"Part I: {total_winnings}")

	joker = True
	card_sorted = get_card_rank(card_bid, joker=joker)
	total_winnings = get_total_winnings(card_sorted)
	print(f"Part II: {total_winnings}") 


if __name__ == "__main__":
	main()
