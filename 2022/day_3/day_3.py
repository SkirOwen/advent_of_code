from itertools import zip_longest
from typing import Iterable, Tuple, List

# also availbale with `python -m pip install more-itertools`
def grouper(iterable, n, *, incomplete='fill', fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    if incomplete == 'fill':
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == 'strict':
        return zip(*args, strict=True)
    if incomplete == 'ignore':
        return zip(*args)
    else:
        raise ValueError('Expected fill, strict, or ignore')


def split_two(line: Iterable) -> Tuple:
	half_point = len(line) // 2
	return line[:half_point], line[half_point:]


def rget_matching_letter(lines: Iterable) -> str:
	if len(lines) == 2:
		match = set(lines[0]) & set(lines[1])
	else:
		match = rget_matching_letter([lines[0], rget_matching_letter(lines[1:])])
	return "".join(match)


def get_item_priority(letter: str) -> int:
	# "a" should give 1 and "A" 27
	unicode_shift = -38 if letter.isupper() else -96
	return ord(letter) + unicode_shift


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = f.read().splitlines()

	# Part One
	lst_priority = []
	for line in lines:
		fst_half, scd_half = split_two(line)

		match = rget_matching_letter([fst_half, scd_half])
		lst_priority.append(get_item_priority(match))

	print(sum(lst_priority))

	# Part Two
	lst_badges = []
	for backback_grp in grouper(lines, 3):
		match = rget_matching_letter(backback_grp)
		lst_badges.append(get_item_priority(match))

	print(sum(lst_badges))


if __name__ == '__main__':
	main()
