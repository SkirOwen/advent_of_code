from __future__ import annotations

import math


def get_races(lines: list[str, str]) -> list[tuple[int, int]]:
	time_str = lines[0]
	dist_str = lines[1]

	time_val = time_str.split(":")[1].strip().split()
	time_lst = list(map(int, time_val))

	dist_val = dist_str.split(":")[1].strip().split()
	dist_lst = list(map(int, dist_val))

	races = [(t, d) for t, d in zip(time_lst, dist_lst)]
	return races


def race_option(race: tuple[int, int]) -> list[int]:
	options = 0
	time = race[0]
	rec_dist = race[1]

	for t in range(time + 1):
		speed = t
		dist = (speed * (time - t))

		if dist > rec_dist:
			options += 1

	return options 


def get_races_options(races: list[tuple[int, int]]) -> list[list[int]]:
	dist =[]
	for i, race in enumerate(races, start=1):
		print(f"Race {i}")
		dist.append(race_option(race))
	return dist


def fix_kerning(races: list[tuple[int, int]]) -> list[tuple[int, int]]:
	time = "".join([str(r[0]) for r in races])
	dist = "".join([str(r[1]) for r in races])

	races_fixed = [(int(time), int(dist))]
	print(races_fixed)
	return races_fixed


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	races = get_races(lines)
	print(races)
	options = get_races_options(races)
	print(options)
	print(f"Part I: {math.prod(options)}")

	races_fixed = fix_kerning(races)
	options_fixed = get_races_options(races_fixed)
	print(options_fixed)
	print(f"Part II: {math.prod(options_fixed)}")


if __name__ == "__main__":
	main()
