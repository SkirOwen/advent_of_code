from __future__ import annotations


def combine_near_digits(idx_nbr: list[int, str]) -> dict[int, str]:
	"""
	Combine nearby digits.
	When parsing the lines, the digits are parser individually.
	This will put them back together.
	The position of the number will be the position of the left most digit.
	The number returned in the dict is a string so it is easy to
	get the len of the number and thus the full coordinates.


	Example
	-------
	idx_nbr = [(61, '1'), (62, '1'), (63, '1'), (82, '4'), (83, '9'), (84, '5'), (100, '5'), (101, '5'), (102, '8')]
	combine_near_digtis(idx_nbr)
	>>> {61: "111", 82: "495", 100: "558"} 
	"""
	combined_idx_nbr = dict()

	i_prev, nbr_prev = idx_nbr[0]
	i_start_nbr = i_prev
	combined_nbr = nbr_prev

	for i, nbr in idx_nbr[1:]:
		if i == i_prev + 1:
			combined_nbr += nbr
		else:
			combined_idx_nbr[i_start_nbr] = combined_nbr
			combined_nbr = nbr
			i_start_nbr = i

		i_prev = i
	# Last one to catch the last one in the loop.
	combined_idx_nbr[i_start_nbr] = combined_nbr

	return combined_idx_nbr


def parse_line(line: str) -> tuple[list[int], dict[int, str]]:

	idx_nbr = []
	idx_gear = []

	for i, c in enumerate(line):
		if c.isdigit():
			# Storing the individual number in a list so after can easily combine them
			idx_nbr.append((i, c))
		elif c == "*":
			idx_gear.append(i)

	if len(idx_nbr) != 0:
		idx_nbr = combine_near_digits(idx_nbr)
	print(f"{idx_gear = }")

	return idx_gear, idx_nbr


def parse_lines(lines: list[str]):
	gears = []
	numbers = []

	for i, line in enumerate(lines):
		idx_gears, idx_nbr = parse_line(line)
		gears.append(idx_gears)
		numbers.append(idx_nbr)
	print(gears)

	return gears, numbers


def is_symb_near(pos: tuple(int), nbr: str, grid: list) -> bool:
	nbr_size = len(nbr)
	row, col = pos
	nbr_end = col + nbr_size - 1

	at_top = row == 0
	at_bottom = row == len(grid) - 1
	at_left = col == 0
	at_right = nbr_end == len(grid[0]) - 1

	adj = []

	if not at_right:
		right = grid[row][nbr_end + 1]
		adj.append(right)

	if not at_top:
		ups =   grid[row - 1][col: nbr_end + 1]
		adj.append(ups)
	
	if not at_left:
		left =  grid[row][col - 1]
		adj.append(left)

	if not at_bottom:
		downs = grid[row + 1][col: nbr_end + 1]
		adj.append(downs)

	if not at_top and not at_right:
		ur = grid[row - 1][nbr_end + 1]
		adj.append(ur)

	if not at_top and not at_left:
		ul = grid[row - 1][col - 1]
		adj.append(ul)

	if not at_bottom and not at_left:
		dl = grid[row + 1][col - 1]
		adj.append(dl)

	if not at_bottom and not at_right:
		dr = grid[row + 1][nbr_end + 1]
		adj.append(dr)

	adj = "".join(adj)
	is_near = any(a not in [".", "1", "2", "3", "4", "5", "6", "7", "8", "9"] for a in adj)
	return is_near


def get_valide_nbr(numbers, grid) -> list[int]:
	valide_nbr = []
	for i, number_line in enumerate(numbers):
		if len(number_line) == 0:
			continue
		for idx, nbr in number_line.items():
			pos = (i, idx)
			if is_symb_near(pos, nbr, grid):
				valide_nbr.append(int(nbr))
	return valide_nbr



def nbr_near_gear(gear_pos, numbers):
	gear_row, gear_col = gear_pos
	print(f"{gear_pos = }")

	row_nbr_near = []
	near_rows = [gear_row - 1, gear_row, gear_row + 1]
	nbr_pos = []
	nbrs = []

	for r in near_rows:
		if 0 < r < len(numbers):
			if len(numbers[r]) >= 0:
				print("a")
				row_nbr_near.append(r)

	col_nbr_near = []
	near_cols = [gear_col - 1, gear_col, gear_col + 1]
		
	for c in near_cols:
		nbr_r = [numbers[i] for i in row_nbr_near]
		print("r", nbr_r)
		for nbr_c in nbr_r:
			print("nbrc", nbr_c)
			if c in nbr_c:
				print("c", c)
				print("appended")
				nbr_pos.append((r, c))
				print("n", numbers[r])
				# nbrs.append(numbers[r][c])

	print(row_nbr_near)
	print(nbr_pos)




def valide_gear(gears, numbers) -> list[int]:
	
	for r, gear_row in enumerate(gears):
		for gear_col in gear_row:
			gear_pos = (r, gear_col)
			nbr_near_gear(gear_pos, numbers)




def main() -> None:
	filename = "test.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	gears, numbers = parse_lines(lines)

	valide_nbr = get_valide_nbr(numbers, lines)
	print(f"Part I: {sum(valide_nbr)}")

	near_gear_nbr = valide_gear(gears, numbers)


if __name__ == "__main__":
	main()
