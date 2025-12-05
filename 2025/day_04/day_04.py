from __future__ import annotations

import time


def draw(lines, free: list, clear):
	RED = "\033[0;31m"
	GREEN = "\033[0;32m"
	BROWN = "\033[0;33m"
	BLUE = "\033[0;34m"
	END = "\033[0m"

	for y, line in enumerate(lines):
		for x, c in enumerate(line):
			if (x, y) in free:
				print(f"{RED}{c}{END}", end="")
			else:
				print(c, end="")
		print()

	if clear:
		time.sleep(0.001)
		print("\033[1A" * len(lines), end="\x1b[2K")



def find_rolls(lines, recurse: bool = False):
	total = 0

	clear = True if recurse else False

	accessible_rolls = []

	y_max = len(lines)
	x_max = len(lines[0])

	def check_access(x, y):
		neighbours_free = 0


		directions = {
			"up": (x, y-1),			
			"ur": (x+1, y-1),			
			"ri": (x+1, y),			
			"dr": (x+1, y+1),			
			"do": (x, y+1),			
			"dl": (x-1, y+1),			
			"le": (x-1, y),			
			"ul": (x-1, y-1),
		}

		for new_loc in directions.values():

			if new_loc[0] < 0 or new_loc[1] < 0 or new_loc[0] >= x_max or new_loc[1] >= y_max:
				neighbours_free += 1
			else:
				if lines[new_loc[1]][new_loc[0]] != "@":
					neighbours_free += 1

		accessible = neighbours_free > 4
		# print(neighbours_free)

		return accessible

	while True:
		rolls_removed = 0

		for y, line in enumerate(lines):
			for x, roll in enumerate(line):
				if roll == "@":
					if check_access(x, y):
						rolls_removed += 1
						accessible_rolls.append((x, y))

		total += rolls_removed

		draw(lines, accessible_rolls, clear)

		if not recurse:
			break
		if rolls_removed == 0:
			break

		for roll_x, roll_y in accessible_rolls:
			lines[roll_y][roll_x] = "."

		
	return total


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [list(line.strip()) for line in f]

	for line in lines:
		print(line)

	total = find_rolls(lines)

	print(total)
	print("--")

	total_2 = find_rolls(lines, recurse=True)
	print(total_2)


if __name__ == "__main__":
	main()
