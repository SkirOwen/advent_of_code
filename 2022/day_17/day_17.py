from itertools import cycle
from typing import List, Dict, Tuple


def falling_tower(rocks: List, winds: List, nbr_fallen: int) -> List:
	fallen_rocks = []
	rock_nbrs = []

	wind_cycle = cycle(winds)
	new_ground = 0
	wind_nbr = 0

	for rock_nbr, rock in enumerate(cycle(rocks), start=1):
		flag = False

		if rock_nbr % len(rocks) == 0 and wind_nbr % len(rocks) == 0:
			flag = True

		starting_position = complex(2, new_ground + 3)
		# print(rock)

		rock_position = [starting_position + rock_pos for rock_pos in rock]
		# print(rock_position)
		is_moving = True

		while is_moving:
			wind = next(wind_cycle)
			wind_nbr += 1
			# print(rock_nbr, w, wind)
			mov = 0
			if wind == "<":
				mov = -1

			elif wind == ">":
				mov = 1

			new_position = [pos + mov for pos in rock_position]
			place_free = all(new_pos not in sum(fallen_rocks[-20:], []) for new_pos in new_position)
			
			if all(0 <= new_pos.real < 7 for new_pos in new_position) and place_free:
				rock_position = new_position
			# 	print("moved")

			# print(rock_position)

			fall_posistion = [pos - 1j for pos in rock_position]
			place_free = all(fall_pos not in sum(fallen_rocks[-20:], []) for fall_pos in fall_posistion)
			# print(fall_posistion)
			# print(sum(fallen_rocks, []))
			# print(f"{place_free = }")

			if all(0 <= fall_pos.imag for fall_pos in fall_posistion) and place_free:
				# print("fell")
				rock_position = fall_posistion
			else:
				# print("a")
				is_moving = False
				break

		# if rock_nbr % 100 == 0:
		# 	print(rock_nbr)
		# if flag:
		# 	print(rock_position)

		fallen_rocks.append(rock_position)
		rock_nbrs.append(rock_nbr)
		new_ground = max([pos.imag for pos in sum(fallen_rocks[-20:], [])]) + 1

		# print(rock_nbr)
		# print("")
		if rock_nbr >= nbr_fallen:
			break

	return fallen_rocks, rock_nbrs


def draw(fallen_rocks: List) -> List:
	tower_height = int(max([pos.imag for pos in sum(fallen_rocks, [])]) + 4)
	colours = ["\033[0;97m", "\033[0;33m", "\033[0;35m", "\033[0;92m", "\033[0;31m"]
	reset_colour = "\033[0m"

	grid = [["." for i in range(7)] for j in range(tower_height)]	# Gen the grid

	for rock, colour in zip(fallen_rocks, cycle(colours)):			# filling the grid with rocks with one colour per rock type
		for pos in rock:
			x, y = int(pos.real), -int(pos.imag)-1
			grid[y][x] = colour + "#" + reset_colour

	bin_lst = []

	for i, row in enumerate(grid):									
		bin_row_lst = [0 if p == "." else 1 for p in row]			# byte-ising the rows of the grid row-by-row
		bin_row = int("".join(map(str, bin_row_lst)), 2)

		bin_lst.insert(0, bin_row)
		
		row_nbr = str(len(grid) - i-1).rjust(len(str(len(grid))))
		print("|", *row, "|", row_nbr, bin_row)						# printing the grid row by row
	print("+ - - - - - - - +")
	
	return bin_lst


def find_repeat_length(lst: List) -> Tuple:
	fst = lst[0]
	potential_patterns = []
	indices = [i for i, v in enumerate(lst) if v == fst]
	# print(fst, indices)

	for i in indices:
		test_pattern = []
		k = 0
		while True:
			if i + k >= len(lst) - 1:
				break
			test_pattern.append(lst[i+k])
			k += 1
			if i + k in indices:
				break

		potential_patterns.append(test_pattern)

	# for p in potential_patterns:
	# 	print(p)

	# print("== Find pattern ==")
	pattern_indices = find_pattern(potential_patterns)
	# print(pattern_indices)

	pattern_length = len(sum(potential_patterns[pattern_indices[0]: pattern_indices[-1] + 1], []))
	transition_length = len(sum(potential_patterns[:pattern_indices[0]], []))

	k = 1
	while potential_patterns[0][-k] == potential_patterns[pattern_indices[-1]][-k]:
		transition_length -= 1
		k += 1

	# print(pattern_length)
	# print(transition_length)
	return transition_length, pattern_length


def find_pattern(potential_patterns: List) -> List:
	patterns_loc = []
	repeat_loc = []
	for i in range(len(potential_patterns)):
		for k in range(1, len(potential_patterns) - i):
			if (potential_patterns[i] == potential_patterns[i+k]) and (i not in patterns_loc):
				
				patterns_loc.append(i)
				repeat_loc.append(i+k)
				# print(f"pattern at {i} is at {i+k}")

	# print(*patterns_loc)
	# print(*repeat_loc)
	# print("removing dup")

	patterns_loc = set(patterns_loc) - set(repeat_loc)
	repeat_loc = repeat_loc[:len(patterns_loc)]

	# print(*patterns_loc)
	# print(*repeat_loc)
	# Woul not work if pattern like AnBnC where n is random
	# patterns = sum([potential_patterns[i] for i in patterns_loc], [])
	# print(patterns)
	# for i in patterns_loc:
	# 	print(potential_patterns[i])
	# 	print(len(potential_patterns[i]))

	return list(patterns_loc)


def rock_nbrs_per_cycle(fallen_rocks: List, rock_nbrs: List, transition_length: List, pattern_length: List) -> Tuple:
	for n, rock in zip(rock_nbrs, fallen_rocks):
		rock_y = [pos.imag for pos in rock]
		if any([(y == transition_length - 1) for y in rock_y]):
			# print(n)
			rocks_in_trans = n

		if any([(y == transition_length + pattern_length - 1) for y in rock_y]):
			# print(n - rocks_in_trans)
			rock_per_cycle = n - rocks_in_trans

	# print("r", rock_per_cycle, rocks_in_trans)
	return rock_per_cycle, rocks_in_trans


def get_rock_in_undershoot(undershoot_rocks: int, pattern_length: int, rocks_in_pattern: int, transition_length: int, rocks_in_trans: int, fallen_rocks: List, rock_nbrs: List) -> int:
	# count height of undershoot rocks in pattern
	starting_rock_pattern = fallen_rocks[rocks_in_trans]
	# need to take the height after the next undershoot_rock
	last_rock = fallen_rocks[rocks_in_trans + undershoot_rocks - 1]
	z_last = max([int(pos.imag) for pos in last_rock])
	return z_last - transition_length + 1


def get_height_from_cycle(
		rocks_in_trans: int,
		transition_length: int,
		rocks_in_pattern: int,
		pattern_length: int,
		nbr_fallen: int,
		fallen_rocks: List,
		rock_nbrs: List
	) -> int:
	height = transition_length
	rock_fallen = rocks_in_trans
	k = 0

	repeats = (nbr_fallen - rock_fallen) // rocks_in_pattern
	height += (pattern_length * repeats)
	rock_fallen += (rocks_in_pattern * repeats)

	undershoot_rocks = nbr_fallen - rock_fallen
	# print(rock_fallen)
	# print("u", undershoot_rocks)
	height_undershoot = get_rock_in_undershoot(undershoot_rocks, pattern_length, rocks_in_pattern, transition_length, rocks_in_trans, fallen_rocks, rock_nbrs)
	
	# print(height)
	# print(height + height_undershoot)
	return height + height_undershoot


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = f.readline()

	winds = lines[:-1]
	# print("winds = ", len(winds))

	rocks = [	# lower left is (0, 0)
		[complex(0, 0), complex(1, 0), complex(2, 0), complex(3, 0)],					# -
		[complex(1, 0), complex(0, 1), complex(1, 1), complex(2, 1), complex(1, 2)],	# +	
		[complex(0, 0), complex(1, 0), complex(2, 0), complex(2, 1), complex(2, 2)],	# _|
		[complex(0, 0), complex(0, 1), complex(0, 2), complex(0, 3)],					# |
		[complex(0, 0), complex(1, 0), complex(0, 1), complex(1, 1)]					# ::
	]

	# Part One
	nbr_to_fall = 10000
	fallen_rocks, rock_nbrs = falling_tower(rocks, winds, nbr_to_fall)

	tower_height = int(max([pos.imag for pos in sum(fallen_rocks, [])]) + 1)
	print(f"tower height after {nbr_to_fall}: {tower_height}")
	bin_lst = draw(fallen_rocks)

	# Part Two
	transition_length, pattern_length = find_repeat_length(bin_lst)
	print(transition_length, pattern_length, pattern_length + transition_length)

	rocks_in_pattern, rocks_in_trans = rock_nbrs_per_cycle(fallen_rocks, rock_nbrs, transition_length, pattern_length)

	nbr_to_fall = 1_000_000_000_000
	# nbr_to_fall = 2022
	height = get_height_from_cycle(rocks_in_trans, transition_length, rocks_in_pattern, pattern_length, nbr_to_fall, fallen_rocks, rock_nbrs)
	print(height)


if __name__ == "__main__":
	main()
