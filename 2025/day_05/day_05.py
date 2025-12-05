from __future__ import annotations
import os

from operator import methodcaller


def find_fresh(id_fresh, ingredients):
	nbr_fresh = 0

	for ingredient in ingredients:
		is_fresh = False

		for id_rg in id_fresh:
			if id_rg[0] <= ingredient <= id_rg[1]:
				is_fresh = True

		if is_fresh:
			nbr_fresh += 1

	return nbr_fresh


def remove_overlap(id_fresh):

	new_ids = set()

	for id_rg in id_fresh:
		candidate = list(id_rg)

		while True:
			test_cand = candidate.copy()

			for new in id_fresh:
				if new[0] < candidate[0] and new[1] >= candidate[0]:
					candidate[0] = new[0]
				
				if new[1] > candidate[1] and new[0] <= candidate[1]:
					candidate[1] = new[1]
			
			if test_cand == candidate:
				break

		new_ids.add(tuple(candidate))

	return new_ids


def count_fresh(id_fresh):

	count = 0

	id_fresh = remove_overlap(id_fresh)

	for id_rg in id_fresh:

		count += id_rg[1] - id_rg[0] + 1

	return count
 

def parse(lines):
	break_idx = lines.index("")

	id_fresh = lines[:break_idx]
	ingredients = list(map(int, lines[break_idx+1:]))

	id_fresh = list(
		map(lambda s: tuple(map(int, methodcaller("split", "-")(s))), id_fresh)
	)

	return id_fresh, ingredients


def main() -> None:
	filename = os.path.join(os.path.dirname(__file__), "input.txt")

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	# print(lines)

	id_fresh, ingredients = parse(lines)
	# print(ingredients)

	nbr_fresh = find_fresh(id_fresh, ingredients)
	print(nbr_fresh)

	fresh_count = count_fresh(id_fresh)
	print(fresh_count)


if __name__ == "__main__":
	main()
