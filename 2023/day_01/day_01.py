from __future__ import annotations

import re


def str2nbr(word: str) -> str:
	match word:
		case "one":
			return "1"
		case "two":
			return "2"
		case "three":
			return "3"
		case "four":
			return "4"
		case "five":
			return "5"
		case "six":
			return "6"
		case "seven":
			return "7"
		case "eight":
			return "8"
		case "nine":
			return "9"
		case _:
			return word


def extracting_numbers(line: str, letters2nbr: bool = False) -> int:
	"""
	Parameters
	----------
	line : str,
		line to parse
	letters2nbr : bool, optional
		If True, interperts spelled out number as numbers. e.g. 'one' is 1.
	"""
	if letters2nbr:
		regx_pattern = r"(?=(\d+|one|two|three|four|five|six|seven|eight|nine))"
	else:
		regx_pattern = r'(?=(\d+))'

	all_line_numbers = [m.group(1) for m in re.finditer(regx_pattern, line)]
	# print(all_line_numbers)

	if letters2nbr:
		all_line_numbers = list(map(str2nbr, all_line_numbers))
	# print(all_line_numbers)

	all_line_numbers = "".join(n for n in all_line_numbers)

	number = all_line_numbers[0] + all_line_numbers[-1]
	# print(line, all_line_numbers, number)
	return int(number)


def extracting_all_numbers(
	lines: list[str],
	letters2nbr: bool = False
) -> list[int]:
	"""Helper function to loop through all lines"""
	numbers = [extracting_numbers(line, letters2nbr) for line in lines]
	return numbers


def main() -> None:
	filename = "input.txt"

	lines = []

	with open(filename, "r") as f:
		for line in f:
			lines.append(line.strip())


	print("------")
	numbers = extracting_all_numbers(lines)
	print(f"Part I: {sum(numbers)}\n")

	numbers_with_letters = extracting_all_numbers(lines, letters2nbr=True)
	# print(numbers_with_letters)
	print("------")
	print(f"Part II: {sum(numbers_with_letters)}\n")


if __name__ == "__main__":
	main()
