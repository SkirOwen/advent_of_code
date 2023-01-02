import re
from typing import List, Dict


def line_parser(line: str) -> List:
	sparsed_line = list(map(int, re.split(",|\n", line)[:-1]))
	return sparsed_line


def get_cubes_faces(cubes) -> Dict:
	faces = {}
	for cube in cubes:
		x, y, z = cube
		up = (x, y, z + 0.5)
		down = (x, y, z - 0.5)
		left = (x - 0.5, y, z)
		right = (x + 0.5, y, z)
		front = (x, y - 0.5, z)
		back = (x, y + 0.5, z)
		faces[str(cube)] = [up, down, left, right, front, back]
	return faces


def count_visible_faces(faces: Dict) -> int:
	all_faces = sum([v for k, v in faces.items()], [])
	visible_faces = [face for face in all_faces if all_faces.count(face) == 1]
	return len(visible_faces)


def check_in_hull(cubes: List, point: List) -> bool:
	# https://stackoverflow.com/a/43564754/9931399
	# method using convex combination
	# linprog min c 
	from scipy.optimize import linprog

	n_cubes = len(cubes)
	n_dim = len(point)
	c = [0 for i in range(n_cubes)]
	A = [[cube[k] for cube in cubes] for k in range(n_dim)]
	A.append([1 for i in range(len(cubes))])
	b = point + [1]
	lp = linprog(c, A_eq=A, b_eq=b)
	return lp.success


def get_inside_cubes(cubes: List) -> List:
	point_inside_hull = []
	x_min = min([cube[0] for cube in cubes])
	x_max = max([cube[0] for cube in cubes])
	y_min = min([cube[1] for cube in cubes])
	y_max = max([cube[1] for cube in cubes])
	z_min = min([cube[2] for cube in cubes])
	z_max = max([cube[2] for cube in cubes])

	print("checking hull")
	for z in range(z_min, z_max + 1):
		for y in range(y_min, y_max + 1):
			for x in range(x_min, x_max + 1):
				point = [x, y, z]
				if (point not in cubes) and check_in_hull(cubes, point):
					point_inside_hull.append(point)
	
	candidate_point = point_inside_hull.copy()
	
	while True:		
	# looping to remove potential "shelling" on the side of the hull that would still be counted
	# in the hull
	# Since the convex hull is defined as the most exterior points 
		inside_cubes = []
		for point in candidate_point:
			x, y, z = point
			sides = [[x, y, z+1], [x, y, z-1], [x, y+1, z], [x, y-1, z], [x+1, y, z], [x-1, y, z]]
			is_next_to_air = all([((side in cubes) or (side in candidate_point)) for side in sides])
			
			if is_next_to_air: 	# it there empty space next to point_inisde_hull
				inside_cubes.append(point)

		if len(candidate_point) == len(inside_cubes):
			break

		candidate_point = inside_cubes.copy()
	return inside_cubes


def main() -> None:
	filename = "input.txt"

	cubes = []

	with open(filename, "r") as f:
		for line in f:
			cubes.append(line_parser(line))

	# Part One
	# print(cubes)
	faces = get_cubes_faces(cubes)
	visible_faces = count_visible_faces(faces)
	print(f"{visible_faces = }")

	# Part Two
	inside_cubes = get_inside_cubes(cubes)
	print(f"Number of air cube inside the lava: {len(inside_cubes)}")

	faces_inside = get_cubes_faces(inside_cubes)
	visible_inside = count_visible_faces(faces_inside)

	print(f"Faces exposed to inside air: {visible_inside}")
	print(f"Faces exposed to only outside: {visible_faces - visible_inside}") 


if __name__ == "__main__":
	main()
