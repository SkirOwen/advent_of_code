from __future__ import annotations

import math


def get_min_game_possible(game: list) -> tuple(int, int, int):
	# print(game)
	run_red = [run[0] for run in game]
	run_green = [run[1] for run in game]
	run_blue = [run[2] for run in game]

	min_possible = (max(run_red), max(run_green), max(run_blue))
	# print(min_possible)

	return min_possible


def get_powers_games(games: dict) -> list[int]:
	powers = []
	for game_id, runs in games.items():
		power = math.prod(get_min_game_possible(runs))
		powers.append(power)

	return powers


def is_game_possible(game: list, criteria: tuple = (12, 13, 14)) -> bool:
	"""
	Criteria is the condion for the game to be possible.
	The max number of red, green, and blue cubes in the bag.
	By default, this is 12, 13, 14.
	"""
	for run in game:
		for colour in range(3):
			if run[colour] > criteria[colour]:
				return False
	return True


def get_id_possible_games(games: dict) -> list[int]:
	possible_games = []

	for game_id, runs in games.items():
		if is_game_possible(runs):
			possible_games.append(int(game_id))
	
	return possible_games


def parse_run(run: str) -> tuple[int, int, int]:
	red, green, blue = 0, 0, 0
	cube_colours = run.split(", ")
	# The colour of cube are not always in the same order
	for cube_colour in cube_colours:
		nbr, colour = cube_colour.split()

		if colour == "red":
			red = int(nbr)
		if colour == "green":
			green = int(nbr)
		if colour == "blue":
			blue = int(nbr)

	return (red, green, blue)


def parse_games(lines) -> dict:
	games = dict()

	for line in lines:
		# Getting the id of the game from "Game #: "
		game_info, cubes_info = line.split(": ")
		game_id = game_info.split()[1]

		cubes_runs = cubes_info.split("; ")
		runs = []
		# n nbrs of sets of cubes per games
		for i, run in enumerate(cubes_runs):
			runs.append(parse_run(run.strip()))

		games[game_id] = runs
	return games


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	games = parse_games(lines)

	possible_games = get_id_possible_games(games)
	print(f"Part I: {sum(possible_games)}\n")

	powers_games = get_powers_games(games)
	# print(powers_games)
	print(f"Part II: {sum(powers_games)}")


if __name__ == "__main__":
	main()
