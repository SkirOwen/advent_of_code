from __future__ import annotations


def parse_lines(lines: list) -> tuple[list, list]:
	towels = lines[0].split(", ")
	patterns = lines[2:]
	return towels, patterns


def check_patterns_possible(patterns: list[str], towels: list[str]) -> dict[str, int]:
	matches = {}

	for pattern in patterns:
		c = check_pattern_possible(pattern, towels)
		matches[pattern] = c
	return matches


def check_pattern_possible(pattern: str, towels: list[str]) -> list[int]:
	dp = [0] * (len(pattern) + 1)
	dp[0] = 1  # One way to form an empty string: using no substrings

	# Iterate through each character position in the pattern
	for i in range(1, len(pattern) + 1):
		for towel in towels:
			if i >= len(towel) and pattern[i - len(towel):i] == towel:
				dp[i] += dp[i - len(towel)]

	return dp[len(pattern)]



def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	towels, patterns = parse_lines(lines)
	towels = sorted(towels, key=len, reverse=True)

	matches = check_patterns_possible(patterns, towels)
	result1 = sum(1 for value in matches.values() if value != 0)
	result2 = sum(value for value in matches.values())


	print(f"Part I: {result1}")

	print(f"Part II: {result2}")


if __name__ == "__main__":
	main()
