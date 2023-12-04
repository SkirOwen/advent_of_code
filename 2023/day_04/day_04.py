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

	for card_id, line in enumerate(lines):
		win_nbr, nbr = parse_card(line)
		matching_nbrs = get_matching_nbr(win_nbr, nbr)
		cards.append(card_id)

		print(len(matching_nbrs))
		print(f"card {card_id}\n{len(matching_nbrs)}")
		for j in range(card_id + 1, card_id + len(matching_nbrs) + 1):
			print(j)

		print("---")

	return points


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	# parse_card(lines[1])
	points = point_for_cards(lines)
	print(points)
	print(f"Part I: {sum(points)}\n")

	all_cards = get_copy_cards(lines)
	print(f"Part II: {len(all_cards)}")


if __name__ == "__main__":
	main()
