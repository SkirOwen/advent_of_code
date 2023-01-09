import re

from itertools import cycle
from time import sleep


def line_parser(lines: list) -> tuple[list, list]:
	separator_idx = lines.index("\n")

	instruction = lines[separator_idx+1].split()[0]
	instruction = re.split("(\d+)", instruction)[1:-1]
	drawing = lines[:separator_idx]

	open_tiles = []
	walls = []
	
	for y, line in enumerate(drawing, start=1):
		for x, c in enumerate(line, start=1):
			if c == ".":
				open_tiles.append(complex(x, y))
			if c == "#":
				walls.append(complex(x, y))

	# for w in walls:
	# 	print(w)
	return [open_tiles, walls], instruction


def find_wrap_tile(mov: complex, pos: complex, open_tiles: list[complex], walls: list[complex]) -> complex:
	a, b = int(pos.real), int(pos.imag)
	all_tiles = open_tiles + walls

	# left/right: imag cst
	if mov.imag == 0:
		open_pos = [v.real for v in all_tiles if v.imag == b]
		if a == min(open_pos):
			new_a = max(open_pos)
		else:	# i.e a > pos 	cause a not in open_pos
			new_a = min(open_pos)
		new_pos = complex(new_a, b)
	# up/down:	real cst
	else:
		open_pos = [v.imag for v in all_tiles if v.real == a]
		if b == min(open_pos):
			new_b = max(open_pos)
		else:
			new_b = min(open_pos)
		new_pos = complex(a, new_b)

	return new_pos


def get_face_neighbours(face_idx: dict, face_div: float) -> dict:
	face_coor = {v: k for k, v in face_idx.items()}
	face_neighbours = {}

	for i in range(1, 6+1):
		face = face_coor[i]
		# if row/col +-2 and same col/row => NO
		opposite_faces = [face + 2, face - 2, face + 2j, face - 2j]

		for opposite_face in opposite_faces:
			if opposite_face in face_idx:
				opposite_idx = face_idx[opposite_face]

		# if row/col +-2 and col/row +-1 and is (row/col +-1, col/row +-1) => NO 
		opposite_faces = [
			[face + complex(2, 1), face + complex(1, 1), face + 1],
			[face + complex(-2, 1), face + complex(-1, 1), face - 1],
			[face + complex(2, -1), face + complex(1, -1), face + 1],
			[face + complex(-2, -1), face + complex(-1, -1), face - 1],

			[face + complex(1, 2), face + complex(1, 1), face + 1j],
			[face + complex(-1, 2), face + complex(-1, 1), face + 1j],
			[face + complex(1, -2), face + complex(1, -1), face - 1j],
			[face + complex(-1, -2), face + complex(-1, -1), face - 1j],
		]
		# print(opposite_faces)
		for opposite_face in opposite_faces:
			if (opposite_face[0] in face_idx) and (opposite_face[1] in face_idx) and (opposite_face[2] in face_idx):
				opposite_idx = face_idx[opposite_face[0]]
		
		opposite_faces = [
			[face + complex(2, 2)  , face + complex(0, 1) , face + complex(1, 1)  , face + complex(2, 1)],
			[face + complex(-2, 2) , face + complex(0, 1) , face + complex(-1, 1) , face + complex(-2, 1)],
			[face + complex(2, -2) , face + complex(0, -1), face + complex(1, -1) , face + complex(2, -1)],
			[face + complex(-2, -2), face + complex(0, -1), face + complex(-1, -1), face + complex(-2, -1)],

			[face + complex(2, 2)  , face + complex(1, 0) , face + complex(1, 1)  , face + complex(1, 2)],
			[face + complex(-2, 2) , face + complex(-1, 0), face + complex(-1, 1) , face + complex(-1, 2)],
			[face + complex(2, -2) , face + complex(1, 0) , face + complex(1, -1) , face + complex(1, -2)],
			[face + complex(-2, -2), face + complex(-1, 0), face + complex(-1, -1), face + complex(-1, -2)],
		]
		# print(opposite_faces)
		for opposite_face in opposite_faces:
			if (opposite_face[0] in face_idx) and (opposite_face[1] in face_idx) and (opposite_face[2] in face_idx) and (opposite_face[3] in face_idx):
				opposite_idx = face_idx[opposite_face[0]]
		
		# not checking for two cases:
		#   .              .
		#   . . . .  and   . . . .
		#         .            .

		# print("o", opposite_idx) 
		face_neighbours[i] = [[n] for n in range(1, 6+1) if n != opposite_idx and n != i]
		# print(face_neighbours)

		for k, neighbour in enumerate(face_neighbours[i]):
			# Only using the example net and my input net
			if face_div == 4.25:
				direction = {
					1: {2: (3, 3, True) , 3: (2, 3, False), 4: (1, 3, False), 6: (0, 0, True)},
					2: {1: (3, 3, True) , 3: (0, 2, False), 5: (1, 1, True) , 6: (2, 1, True)},
					3: {1: (3, 2, False), 2: (2, 0, False), 4: (0, 2, False), 5: (1, 2, True)},
					4: {1: (3, 1, False), 3: (2, 0, False), 5: (1, 3, False), 6: (0, 3, True)},
					5: {2: (1, 1, True) , 3: (2, 1, True) , 4: (3, 1, False), 6: (0, 2, False)},
					6: {1: (0, 0, True) , 2: (1, 2, True) , 4: (3, 0, True) , 5: (2, 0, False)},
				}
			else:
				direction = {
					1: {2: (0, 2, False), 3: (1, 3, False), 4: (2, 2, True) , 6: (3, 2, False)},
					2: {1: (2, 0, False), 3: (1, 0, False), 5: (0, 0, True) , 6: (3, 1, False)},
					3: {1: (3, 1, False), 2: (0, 1, False), 4: (2, 3, False), 5: (1, 3, False)},
					4: {1: (2, 2, True) , 3: (3, 2, False), 5: (0, 2, False), 6: (1, 3, False)},
					5: {2: (0, 0, True) , 3: (3, 1, False), 4: (2, 1, False), 6: (1, 0, False)},
					6: {1: (2, 3, False), 2: (1, 3, False), 4: (3, 1, False), 5: (0, 1, False)},
				}
			face_neighbours[i][k].extend(direction[i][neighbour[0]])

	# print("f", face_neighbours)

	return face_neighbours


def find_cube_net(all_tiles: list) -> dict:
	
	face_div = 50.25 if (len(all_tiles) % 50 == 0) else 4.25	
	# check bigger mod first to avoid len being multiple of small and big
	# .25 because so 1,2,3,4 match to 1 and 5,6,7,8 match to 2 and so on...

	net = {}
	set_net = set()
	for v in all_tiles:
		a, b = int(v.real), int(v.imag)
		a1 = int(a // (face_div) + 1)
		b1 = int(b // (face_div) + 1)
		net[v] = (complex(a1, b1)) 
		set_net.add(complex(a1, b1))

	face_idx = {v: k for k, v in enumerate(set_net, start=1)}
	face_mod_id = {k: v for k, v in enumerate(set_net, start=1)}
	# print("a", face_idx)
	# print("")
	face_neighbours = get_face_neighbours(face_idx, face_div)
	# print("")

	all_net = {k: face_idx[v] for k, v in net.items()}
	# print("n", all_net)
	return all_net, face_mod_id, face_neighbours


def find_cube_wrap(mov: complex, rot: int, pos: complex, open_tiles: list[complex], walls: list[complex]) -> complex:
	all_tiles = open_tiles + walls

	net, face_mod_id, face_neighbours = find_cube_net(all_tiles)
	face_size = 50 if (len(all_tiles) % 50 == 0) else 4
	# canvas = draw([open_tiles, walls], cube_id=net)

	# for row in canvas:
	# 	print(*row)	

	a, b = int(pos.real), int(pos.imag)
	leaving_face = net[pos]
	# print(pos, mov, rot)

	leaving_faces = [face_out[1] for face_out in face_neighbours[leaving_face]]
	cube_wrap = face_neighbours[leaving_face][leaving_faces.index(rot)]
	# print("c", cube_wrap)
	
	leaving_rot = cube_wrap[1]
	arriving_face = cube_wrap[0]
	arriving_rot = cube_wrap[2]
	is_flip = cube_wrap[3]

	leaving_face_coor = face_mod_id[leaving_face]
	arriving_face_coor = face_mod_id[arriving_face]
	# print(arriving_face_coor)

	rel_a = (a % face_size)
	rel_b = (b % face_size)
	# print(a, rel_a, b, rel_b)
	# a and b needs to be the relative position in the new face

	if arriving_rot == 0:
		new_a = arriving_face_coor.real * face_size
		ar_rot = 2
		if leaving_rot == 0:
			new_b = arriving_face_coor.imag * face_size - (rel_b - 1) if is_flip else arriving_face_coor.imag * face_size - face_size + rel_b # cant 00 false
		elif leaving_rot == 1:
			new_b = arriving_face_coor.imag * face_size - (rel_a - 1) if is_flip else arriving_face_coor.imag * face_size - face_size + rel_a #
		elif leaving_rot == 2:
			new_b = arriving_face_coor.imag * face_size - (rel_b - 1) if is_flip else arriving_face_coor.imag * face_size - face_size + rel_b
		else: # leaving_rot == 3
			new_b = arriving_face_coor.imag * face_size - (rel_a - 1) if is_flip else arriving_face_coor.imag * face_size - face_size + rel_a

	elif arriving_rot == 1:
		new_b = arriving_face_coor.imag * face_size
		ar_rot = 3
		if leaving_rot == 0:
			new_a = arriving_face_coor.real * face_size - (rel_b - 1) if is_flip else arriving_face_coor.real * face_size - face_size + rel_b #
		elif leaving_rot == 1:
			# new_a = arriving_face_coor.real * face_size - (rel_a - 1) if is_flip else arriving_face_coor.real * face_size - face_size + rel_a
			new_a = arriving_face_coor.real * face_size - (rel_a - 1) if is_flip else arriving_face_coor.real * face_size - face_size + rel_a
		elif leaving_rot == 2:
			new_a = arriving_face_coor.real * face_size - (rel_b - 1) if is_flip else arriving_face_coor.real * face_size - face_size + rel_b
		else: # leaving_rot == 3
			new_a = arriving_face_coor.real * face_size - (rel_a - 1) if is_flip else arriving_face_coor.real * face_size - face_size + rel_a

	elif arriving_rot == 2:
		new_a = arriving_face_coor.real * face_size - (face_size - 1)
		ar_rot = 0
		if leaving_rot == 0:
			new_b = arriving_face_coor.imag * face_size - (rel_b - 1) if is_flip else arriving_face_coor.imag * face_size - face_size + rel_b
		elif leaving_rot == 1:
			new_b = arriving_face_coor.imag * face_size - (rel_a - 1) if is_flip else arriving_face_coor.imag * face_size - face_size + rel_a
		elif leaving_rot == 2:
			new_b = arriving_face_coor.imag * face_size - (rel_b - 1) if is_flip else arriving_face_coor.imag * face_size - face_size + rel_b #
		else: # leaving_rot == 3
			new_b = arriving_face_coor.imag * face_size - (rel_a - 1) if is_flip else arriving_face_coor.imag * face_size - face_size + rel_a

	else:	# arriving_rot == 3
		new_b = arriving_face_coor.imag * face_size - (face_size - 1)
		ar_rot = 1
		if leaving_rot == 0:
			new_a = arriving_face_coor.real * face_size - (rel_b - 1) if is_flip else arriving_face_coor.real * face_size - face_size + rel_b
		elif leaving_rot == 1:
			new_a = arriving_face_coor.real * face_size - (rel_a - 1) if is_flip else arriving_face_coor.real * face_size - face_size + rel_a
		elif leaving_rot == 2:
			new_a = arriving_face_coor.real * face_size - (rel_b - 1) if is_flip else arriving_face_coor.real * face_size - face_size + rel_b
		else: # leaving_rot == 3
			new_a = arriving_face_coor.real * face_size - (rel_a - 1) if is_flip else arriving_face_coor.real * face_size - face_size + rel_a

	new_pos = complex(new_a, new_b)
	# print(new_pos, ar_rot)
	# print("")

	return new_pos, ar_rot


def follow_instruction(grid: list[list, list], instruction: list, start: list[complex, int], cube: bool = False, drawing: bool = True) -> tuple[complex, int]:
	pos, rot = start
	open_tiles, walls = grid
	all_tiles = open_tiles + walls
	canvas = draw(grid)

	rainbow = cycle(["\033[0;41m", "\033[0;43m", "\033[0;42m", "\033[0;46m", "\033[0;44m", "\033[0;45m"])
	t = 1
	k = -1
	for ins in instruction:
		log = ""
		if ins.isalpha():
			rot = (rot + 1) % 4 if ins == "R" else (rot - 1) % 4
		else:
			for v in range(1, int(ins) + 1):

				if drawing:
					k += 1
					print("\033[1A" * (len(canvas)), end="\x1b[2K")
					if k % 10 == 0:
						colour = next(rainbow)
					canvas = update(canvas, pos, rot, colour)

				if rot == 0:
					mov = 1
				elif rot == 1:
					mov = 1j
				elif rot == 2:
					mov = -1
				else: # rot == 3
					mov = -1j

				new_pos = pos + mov
				new_rot = rot

				if new_pos not in all_tiles:
					if cube:
						new_pos, new_rot = find_cube_wrap(mov, rot, pos, open_tiles, walls)
						# if t == 3:
						# 	return ###########################################################
						# t += 1
					else:
						new_pos = find_wrap_tile(mov, pos, open_tiles, walls)

				if new_pos not in walls:
					if new_pos in open_tiles:
						pos = new_pos
						rot = new_rot
					else:
						break
				else:
					break

		# print(pos, rot, ins, log)
	return pos, rot


def draw(grid: list, cube_id: None | dict = None) -> list:
	y_open = [x.imag for x in grid[0]]
	x_open = [x.real for x in grid[0]]
	y_wall = [x.imag for x in grid[1]]
	x_wall = [x.real for x in grid[1]]

	y_max = int(max(max(y_open), max(y_wall)))
	x_max = int(max(max(x_open), max(x_wall)))

	canvas = [[" " for x in range(x_max + 1)] for y in range(y_max + 1)]

	for open_space in grid[0]:
		a, b = int(open_space.real), int(open_space.imag)
		canvas[b][a] = "." if cube_id is None else str(cube_id[complex(a, b)])

	for wall in grid[1]:
		a, b, = int(wall.real), int(wall.imag)
		canvas[b][a] = "#" if cube_id is None else str(cube_id[complex(a, b)])

	return canvas


def update(canvas: list, position: complex, rot: int, colour: str) -> list:
	orange_back = "\033[0;43m"
	reset_colour = "\033[0m"

	match rot:
		case 0:
			r = ">"
		case 1:
			r = "v"
		case 2:
			r = "<"
		case 3:
			r = "^"

	x, y = int(position.real), int(position.imag)
	canvas[y][x] = colour + r + reset_colour

	for row in canvas:
		print(*row)	

	# sleep(0.1)

	return canvas


def calculate_password(final_pos: tuple[complex, int]) -> int:
	row = int(final_pos[0].imag)
	col = int(final_pos[0].real)
	rot = final_pos[1]
	return (1000 * row) + (4 * col) + rot


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = f.readlines()

	grid, instruction = line_parser(lines)

	start = [grid[0][0], 0]
	# print(start)

	# Part One
	# final_pos = follow_instruction(grid, instruction, start)
	# print(final_pos)
	# password = calculate_password(final_pos)
	# print(password)

	# Part Two

	final_pos = follow_instruction(grid, instruction, start, cube=True, drawing=True)
	print(final_pos)
	password = calculate_password(final_pos)
	print(password)


if __name__ == "__main__":
	main()
