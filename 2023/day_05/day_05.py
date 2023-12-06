from __future__ import annotations

from itertools import pairwise
from typing import Iterable


def grouped(iterable: Iterable, n=2) -> Iterable[tuple]:
    return zip(*[iter(iterable)] * n)


def parse_almanac(lines) -> dict:
	almanac = dict()

	for i, line in enumerate(lines):
		if ":" in line:
			# to do this "seed-to-soil map:" to this "seed-to-soil"
			key = line.split(":")[0].split()[0]

		if i == 0:
			val = list(map(int, line.split(": ")[1].split()))

		elif line == "":
			almanac[key] = val
			val = []

		elif not ":" in line:
			map_range = tuple(map(int, line.split()))
			val.append(map_range)

	almanac[key] = val
	return almanac


def source2destination(source: list[int], destination: list[tuple[int, int, int]]) -> list[int]:
	target = []

	destination_range_start = []
	source_range_start = []
	range_len = []

	for drs, srs, rl in destination:
		destination_range_start.append(drs)
		source_range_start.append(srs)
		range_len.append(rl)

	for s in source:
		for drs, srs, rl in zip(destination_range_start, source_range_start, range_len):
			if srs <= s <= srs + rl - 1:
				target_s = drs + (s - srs)
				target.append(target_s)
				break  # Ugly to break in a for and call an for-else loop, but it works
		else:
			target.append(s)

	return target


def visualisation(source, dest, a, almanac) -> None:
	print(f"----{a}----")
	for s, sr in grouped(source):
		for i in range(sr+s):
			if s < i:
				print("#", end="")
			else:
				print(" ", end="")
		print(s, sr)

	print("")
	print("maps")
	for d, s, sr in almanac[dest]:
		for i in range(sr+s):
			if s < i:
				print("#", end="")
			else:
				print(" ", end="")
		print("")
		print(s, sr)
	print(header)


def seed2loc(almanac: dict, seed_as_range: bool = False) -> list:
	keys = almanac.keys()

	s = almanac["seeds"]
	if seed_as_range:
		s_as_range = []
		for source_start, source_range in grouped(s):
			s_as_range.append([source_start, source_start + source_range])
		s = s_as_range


	for a, d in pairwise(keys):
		if seed_as_range:
			s = source2destination_range(s, almanac[d])
			
		else:
			s = source2destination(s, almanac[d])

	return s


def source2destination_range(source_as_range: list[int], destination: list[tuple[int, int, int]]) -> list:
	target = []

	destination_range_start = []
	source_range_start = []
	range_len = []

	for drs, srs, rl in destination:
		destination_range_start.append(drs)
		source_range_start.append(srs)
		range_len.append(rl)

	while len(source_as_range) > 0:
		source_start, source_end = source_as_range.pop()

		for drs, srs, rl in zip(destination_range_start, source_range_start, range_len):
			overlap_start = max(source_start, srs)
			overlap_end = min(source_end, srs + rl)
			
			if overlap_start < overlap_end:
				target_s = drs + (overlap_start - srs)
				target_e = drs + (overlap_end - srs)
				target.append([target_s, target_e])

				if overlap_start > source_start:
					source_as_range.append([source_start, overlap_start])

				if overlap_end < source_end:
					source_as_range.append([overlap_end, source_end])
				break  # Ugly to break in a for and call an for-else loop, but it works

		else:
			target.append([source_start, source_end])

	return target



def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	almanac = parse_almanac(lines)
	keys = list(almanac.keys())

	loc = seed2loc(almanac)
	print(f"Part I: {min(loc)}")

	loc = seed2loc(almanac, seed_as_range=True)
	print(f"Part II: {min(loc)[0]}")

if __name__ == "__main__":
	main()
