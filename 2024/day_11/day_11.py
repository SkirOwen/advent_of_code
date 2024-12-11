from __future__ import annotations

from tqdm import tqdm

from collections import Counter



def blink(rocks: Counter) -> Counter:
	new_rocks = Counter()

	for rock, qty in rocks.items():
		nbr_digit = len(str(rock))

		if rock == 0:
			new_rocks[1] += qty

		elif nbr_digit % 2 == 0:
			half_idx = nbr_digit // 2
			left = int(str(rock)[:half_idx])
			right = int(str(rock)[half_idx:])
			new_rocks[left] += qty
			new_rocks[right] += qty

		else:
			new_rocks[rock * 2024] += qty

	return new_rocks


def blink_n(lines: list[int], n: int) -> Counter:
	rocks = Counter(lines)

	for i in tqdm(range(n)):
		rocks = blink(rocks)
	return rocks


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [list(map(int, line.strip().split())) for line in f][0]

	# lines = [125, 17]

	print(lines)
	print(Counter(lines))


	result1 = blink_n(lines, n=25)
	print(f"Part I: {sum(result1.values())}")

	result2 = blink_n(lines, n=75)
	print(f"Part II: {sum(result2.values())}")


if __name__ == "__main__":
	main()
