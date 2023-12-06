from __future__ import annotations


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]


if __name__ == "__main__":
	main()
