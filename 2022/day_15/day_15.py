from typing import List, Set, Tuple

from multiprocessing import Pool
from functools import partial

# from tqdm import tqdm


def line_parser(line: str) -> List:
	splitted_line = line.split()
	xs, ys = int(splitted_line[2][2:-1]), int(splitted_line[3][2:-1])
	xb, yb = int(splitted_line[8][2:-1]), int(splitted_line[9][2:])
	sensor = [xs, ys]
	beacon = [xb, yb]
	return [sensor, beacon]


def get_manhattan(x1, x2, y1, y2) -> int:
	return abs(x1 - x2) + abs(y1 - y2)


def get_sensors_radius(sensors: List, beacons: List) -> Tuple:
	sensors_radius = []
	distances = []
	for sensor, beacon in zip(sensors, beacons):
		xs, ys = sensor
		xb, yb = beacon
		distance = get_manhattan(xs, xb, ys, yb)
		top = [xs, ys - distance]
		left = [xs - distance, ys]
		right = [xs + distance, ys]
		down = [xs, ys + distance]

		sensors_radius.append([top, left, right, down])
		distances.append(distance)
	return sensors_radius, distances


def get_nbr_no_beacon(row_to_check: int, sensors: List, sensor_radius: List, distances: List, beacons: List) -> Set:
	places_no_beacons = []
	for sensor, radius, distance in zip(sensors, sensor_radius, distances):
		# print(f"== {sensor} {beacon} ==")
		x = [coor[0] for coor in radius]
		y = [coor[1] for coor in radius]

		min_x = x[1]
		max_x = x[2]

		min_y = y[0]
		max_y = y[3]

		if min_y <= row_to_check <= max_y:
			x_no_beacon_min = sensor[0] - (distance - abs(sensor[1] - row_to_check))
			x_no_beacon_max = sensor[0] + (distance - abs(sensor[1] - row_to_check))

			coor_no_beacon = [i for i in range(x_no_beacon_min, x_no_beacon_max + 1)]
			places_no_beacons.extend(coor_no_beacon)

	return set(places_no_beacons)


def find_empty(max_row_col: int, sensors: List, sensor_radius: List, distances: List, beacons: List) -> None | int:
	check_point = set()

	for sensor, distance, beacon in zip(sensors, distances, beacons):
		print(f"== {sensor} ==")
		xs, ys = sensor

		for direction in range(4):
			for d in range(distance + 1):
				is_found = False

				if direction == 0:		# Top Right
					xp = xs + (distance + 1 - d)
					yp = ys - d

				elif direction == 1:	# Top Left
					xp = xs - (distance + 1 - d)
					yp = ys - d

				elif direction == 2:	# Bottom Left
					xp = xs - (distance + 1 - d)
					yp = ys + d

				else:					# Bottom Right
					xp = xs + (distance + 1 - d)
					yp = ys + d

				if 0 <= xp <= max_row_col and 0 <= yp <= max_row_col and (xp, yp) not in check_point:
					is_found = all(
						get_manhattan(sensors_x, xp, sensors_y, yp) > sen_dis 
						for (sensors_x, sensors_y), sen_dis in zip(sensors, distances)
						)

				if is_found:
					return xp * max_row_col + yp
				else:
					check_point.add((xp, yp))


def main() -> None:
	filename = "input.txt"
	lines = []
	with open(filename, "r") as f:
		for line in f:
			lines.append(line_parser(line))

	sensors = [report[0] for report in lines]
	beacons = [report[1] for report in lines]

	sensor_radius, distances = get_sensors_radius(sensors, beacons)

	# Part One
	row_to_check = 2_000_000
	places_no_beacons = get_nbr_no_beacon(row_to_check, sensors, sensor_radius, distances, beacons)
	print(len(places_no_beacons) - 1)  # 4665948

	# Part Two
	max_row_col = 4_000_000
	tuning_freq = find_empty(max_row_col, sensors=sensors, sensor_radius=sensor_radius, distances=distances, beacons=beacons)
	print(tuning_freq)


if __name__ == "__main__":
	main()
