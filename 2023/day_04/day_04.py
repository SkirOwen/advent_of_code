from __future__ import annotations


def parse_card(line: str) -> tuple[list[int], list[int]]:

	card, nbrs = line.split(":")
	win_nbrs, card_nbrs = nbrs.strip().split("|")

	win_nbrs = list(map(int, win_nbrs.strip().split()))
	card_nbrs = list(map(int, card_nbrs.strip().split()))

	return win_nbrs, card_nbrs


def get_matching_nbr(win_nbrs: list, card_nbrs: list) -> list[int]:

	matching_nbrs = [nbr for nbr in card_nbrs if nbr in win_nbrs]

	return matching_nbrs


def point_for_cards(lines: list) -> list[int]:
	points = []

	for line in lines:
		win_nbr, nbr = parse_card(line)
		matching_nbrs = get_matching_nbr(win_nbr, nbr)

		if len(matching_nbrs) > 0:
			point = 2 ** (len(matching_nbrs) - 1)
		else:
			point = 0
		points.append(point)

	return points


def get_copy_cards(lines: list) -> list:
	# Part II
	cards = []

	for card_id, line in enumerate(lines, start=1):
		win_nbr, nbr = parse_card(line)
		matching_nbrs = get_matching_nbr(win_nbr, nbr)
		copy_of_card = cards.count(card_id) + 1
		
		cards.append(card_id)

		# print(f"card: {card_id} | copy: {copy_of_card} | nbr: {len(matching_nbrs)}")
		for c in range(copy_of_card):
			for j in range(card_id + 1, card_id + len(matching_nbrs) + 1):
				cards.append(j)
				# print(j)

		# print("cards:", sorted(cards))
		# print("---")

	return cards


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	# parse_card(lines[1])
	points = point_for_cards(lines)
	print(points)
	print(f"Part I: {sum(points)}\n")

	all_cards = get_copy_cards(lines)
	# for card in set(all_cards):
	# 	print(card, all_cards.count(card))
	print(f"Part II: {len(all_cards)}")


if __name__ == "__main__":
	main()
