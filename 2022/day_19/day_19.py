import re
import time

from math import prod
from multiprocessing import Pool
from collections import defaultdict
from typing import List, Dict, Tuple


def line_parser(line: str) -> Dict:
	split_line = re.split(" |\n|:", line)
	# print(split_line)
	blueprint = {
		"blueprint": split_line[1],
		"ore_robot": [int(split_line[7]), 0, 0],
		"clay_robot": [int(split_line[13]), 0, 0],
		"obsidian_robot": [int(split_line[19]), int(split_line[22]), 0],
		"geode_robot": [int(split_line[28]), 0, int(split_line[31])]
	}
	return blueprint


def update_state(state: Dict) -> Dict:
	new_state = state.copy()
	# new_state["parent"] = state.copy()
	new_state["time"] += 1
	new_state["ore"] += state["ore_robot"]
	new_state["clay"] += state["clay_robot"]
	new_state["obsidian"] += state["obsidian_robot"]
	new_state["geode"] += state["geode_robot"]
	return new_state


def get_potential_robots(blueprint: Dict, state: Dict, max_robots: Dict) -> List:
	potential_robots = [None]
	all_robot_type = ["ore_robot", "clay_robot", "obsidian_robot", "geode_robot"]
	for robot_type in all_robot_type:
		if robot_possible(blueprint, state, robot_type):
			if robot_type == "geode_robot":
				potential_robots.append(robot_type)
			elif state[robot_type] < max_robots[robot_type]:
				potential_robots.append(robot_type)

	if "geode_robot" in potential_robots:
		return ["geode_robot"]
	return potential_robots


def robot_possible(blueprint: Dict, state: Dict, robot_type: str) -> bool:
	cost = blueprint[robot_type]
	ore_cost, clay_cost, obsidian_cost = cost
	inv_ore = state["ore"]
	inv_clay = state["clay"]
	inv_obsidian = state["obsidian"]
	# print(f"== {robot_type} ==")
	# print("\t", inv_ore, ore_cost)
	# print("\t", inv_clay, clay_cost)
	# print("\t", inv_obsidian, obsidian_cost)
	# print("==")
	
	return (ore_cost <= inv_ore) and (clay_cost <= inv_clay) and (obsidian_cost <= inv_obsidian)


def robot_usefull(blueprint: Dict) -> Dict:
	# dont build more than x mineral if robot need x mineral
	all_robot_type = ["ore_robot", "clay_robot", "obsidian_robot", "geode_robot"]
	ore_mineral_cost = max([blueprint[robot][0] for robot in all_robot_type])
	clay_mineral_cost = blueprint["obsidian_robot"][1]	# only the obsidian robot uses clay
	obsidian_mineral_cost = blueprint["geode_robot"][2]		# only the geode robot uses obsidian

	max_robots = {
		"ore_robot": ore_mineral_cost,
		"clay_robot": clay_mineral_cost,
		"obsidian_robot": obsidian_mineral_cost,
		"geode_robot": None,
	}
	return max_robots


def build_robot_and_update(blueprint: Dict, state: Dict, robot_type: str) -> Dict:
	new_state = state.copy()
	# build
	new_state[robot_type] += 1
	ore_cost, clay_cost, obsidian_cost = blueprint[robot_type]
	new_state["ore"] -= ore_cost
	new_state["clay"] -= clay_cost
	new_state["obsidian"] -= obsidian_cost
	# update
	new_state["time"] += 1
	# new_state["parent"] = state.copy()
	new_state["ore"] += state["ore_robot"]
	new_state["clay"] += state["clay_robot"]
	new_state["obsidian"] += state["obsidian_robot"]
	new_state["geode"] += state["geode_robot"]

	return new_state


def merge_state(built_state: Dict, res_state: Dict) -> Dict:
	new_state = built_state.copy()
	new_state["ore"] += res_state["ore"]
	new_state["clay"] += res_state["clay"]
	new_state["obsidian"] += res_state["obsidian"]
	return new_state


def max_geode_obtain(state: Dict, total_time: int) -> int:
	remaining_time = total_time - state["time"]
	# calculate the max amount of geode if add geode robot every turn until the end
	# comes to do the sum from 0 to remaing time
	amount_robot_add_end = remaining_time * (remaining_time + 1) // 2
	return state["geode"] + remaining_time * state["geode_robot"] + amount_robot_add_end


def max_geode_from_blueprint(blueprint: Dict, total_time: int = 24, return_schemactic: bool = False) -> int:
	init_state = {
			"time": 0,
			"ore": 0,
			"clay": 0,
			"obsidian": 0,
			"geode": 0,

			"ore_robot": 1,
			"clay_robot": 0,
			"obsidian_robot": 0,
			"geode_robot": 0,

			"last_skip": [],
			"parent": None
		}

	stack = [init_state]
	explored_pattern = []
	max_geode = defaultdict(int)
	old_max_geode = defaultdict(int)

	max_robots = robot_usefull(blueprint)
	k = 0
	while stack:
		state = stack.pop(0)
		t = state["time"]

		max_geode[t] = max(state["geode"], max_geode[t])

		if state not in explored_pattern and state["geode"] == max_geode[t]:
			explored_pattern.append(state.copy())

			if state["time"] >= total_time:
				continue

			# print(max_geode_obtain(state, total_time))
			if max_geode_obtain(state, total_time) < max_geode[t]:
				# or state["geode"] != max_geode:
				# comparing the state geode to max works only in depth-first if trying to create geodes bots first
				# print(max_geode_obtain(state, total_time), max_geode)
				continue

			# neighbour are the potential robot, i.e. build no robot, clay, ore, obsi, geode
			potential_robots = get_potential_robots(blueprint, state, max_robots)
			# print(potential_robots)
			for robot_type in potential_robots:
				# if robot_type == "geode_robot":
				# 	print(state)
				# based on the assumption to build a robot if possible
				if robot_type is None:
					pos_state = update_state(state)
					pos_state["last_skip"] = potential_robots
					if pos_state not in stack:
						stack.append(pos_state)
				# print(state["time"])

				elif robot_type in state["last_skip"]:
					# robot_type is never none here
					# prune the branch where did not build a robot when it was possible
					continue

				else:
					pos_state = build_robot_and_update(blueprint, state, robot_type)

					# harvest and needs to be simultaneous

					pos_state["last_skip"] = []
					if pos_state not in stack:
						stack.insert(0, pos_state)
						# if robot_type == "geode_robot":
						# 	print(pos_state)
					
		k += 1
		# max_geode = max(max_geode_)
		if max_geode[t] > old_max_geode[t]:
			old_max_geode[t] = max_geode[t]
			print(k, t, max_geode[t])
			print(len(stack))

	# print(state) 
	if return_schemactic:
		return explored_pattern

	print(blueprint["blueprint"], max([pattern["geode"] for pattern in explored_pattern]))
	return max([pattern["geode"] for pattern in explored_pattern])


def quality_level(max_geode_per_blueprint: List) -> List:
	quality_lvl = []
	for i, v in enumerate(max_geode_per_blueprint, start=1):
		quality_lvl.append(i * v)
	return quality_lvl


def main() -> None:
	filename = "input.txt"

	blueprints = []

	with open(filename, "r") as f:
		for line in f:
			blueprints.append(line_parser(line))

	# print(blueprints[0])
	# max_geode = max_geode_from_blueprint(blueprints[0])

	# Part One
	with Pool(10) as p:
		max_geode_per_bp = p.map(max_geode_from_blueprint, blueprints)

	print(max_geode_per_bp)
	quality_lvl = quality_level(max_geode_per_bp)

	print(sum(quality_lvl))
	
	# Part Two
	max_geode_per_blueprint3 = [max_geode_from_blueprint(bp, 32) for bp in blueprints[:3]]
	print(prod(max_geode_per_blueprint3))


if __name__ == "__main__":
	main()


# line prog approach
# https://topaz.github.io/paste/#XQAAAQBbCgAAAAAAAAA0m0pnuFI8c+qagMoNTEcTIfyUW1xf5cj5UWEFGhQ7Ii8lr4cN5NkhGKvl3n4bZ0aogI13PFfQ1x4u5EQovTXkDFVV8fJvAI0Y3dOKxdxqpCNgsMPQbWmbpulsLc6wiPNSCuB6BhtZJXyyHtbTHOICz1A+KpENLNnFmyb5n8fMUuw1Zz3/GB2nDasX3GkP33bjyEo5J4Nly5CitzkS60IP2tUkTYpxi7WLDgEShCk4gb8RHTRjv5r5IaUivwiDYstRbZLY7HYDOyy0GdaKz2oURXw9xssVNijoPZTxegzFZwJGxXNJgkMagoVjZ5TJLRlSUievK+uF5YHVrGWZpb/VIa9GWcibUeUkTi1Qs/sSEHmC8ZSkpWoWyI498Vn5aVct72gpaXnzCvvdTmH/GEfWDd+7b13bUImV59zclpEzULQxdMNf/aYSsf6WvhNA7E3J+9m3Vcmb74tRtd7WixW0kTeODqX3KjQSQLLZtL0HjrtRt3qXNfbir1+UihiXNUnWmR/CHJnighPYo+6yRakKOaXQweCXNZWt8LQNZ7EKscrqZp1zLvA/M50O40J7ArmHN3Wp3OUhGeAmcRhn54vc0cXynrEZKoDHVk0fTGvJnPovVclYQ791zmMWn5zdMrFrw3FeO7vMZCc3dyPQpCEGcepcvJIkNMEQ0fHlijgmDSvRl6fwwGik6gDzvqLjeC8j6zp4OEo6njwUnHqI0Sw6/IHoWfaI8l7ulqZRB0XrrfXmMNNKmjo+zvjMytqBw0DTlcNpejAMoJVUP+GQZ2JipIhLaM2JWP6dZKYbCLdz79HdoxyKa5LcF5iTjDd6lwQrKy97GBpqmFLiUzv+m6pExi7yF57SPVVbElskVDnOEAclKB2mic43XUUanVksPaDkZguiZ4m8DXzV/618tV6y89TbIHYnx537IOOmd8lsn1cVJyeEV2ibKmRHIOyzVoux/KMZ7qNtkIzCh/0j8jgVm940dhlv721Ji3fLa+EoxS6cQ0gsRCW5hD4bGjy2BnHS4vTxywyKS61H8pJXraSj0OiJLx+PbZqMwwaoiTi//9AQiGE=

# evolution algo
# https://topaz.github.io/paste/#XQAAAQB6CwAAAAAAAAA0m0pnuFI8c+0tjbUheJzfDHhRqAdxWEVwGLaf8mWgSrvnTpK32ky1/T1Sz7nYwK1e3iJqxIUhCsxtrMc5z3SmgWk3ylyIg72S1LcRr75pROZC1rKJmEtT//Vq+mAx3AAKfJbQrPZ0Cp+SuLUJBqT7+UVh2ZIZTMeqsklMzqbIeTmqsJvcb/8i/ZC4jMTvaha3BvXH/S/apYzf4CqlYZg29+SaIcac29A5PXBz89D6K7k+SEItAZ6dtTvNtgYmMf9DSJDtr+x7ZoNZ/bf4hFvSGWtk8BmORmQUhhnDYfaIZkzijUJ2mGEqO76Bqh7ElAt1YflxUXo5XNLcwezOKO0S64x6imavGok62ZwAh8AfI5DzOU8jMwonxxeBaKrl2+CiPw8InqDwYLmzXnNez28sTQztoxtRY0gCemmv54jSerddoBf7zjvdxcIGNhNJR1ijLOq83N9arfqnifUVtwXGMc8oJ5Otjb6f5xfksxeguUCKwFpbWk466x5Xe60vdggPC8C2pfLpQTbZuE//P+MexFDiCgWsuUiL72ynEzpyM7cDpnnsgCqekp9LFwA6duenHP0SmIS/pn55e0P0ZrqOhyH1uxdhsa2hHWDAW9k0lTb/RasGEWNEQSTl1WumzTYXPi1INO+/dtchTpdgeWR1SmNgj3WyLVDQ0Qx10XhnS2xES2/0m6+Ju7/PTOrJqLFvGrCkjDKnchqxDITkZlnjEmXPvN5J9E0UYaD2+kbF33AFNwk8ZQAjdZY22c3OFDgs78S2R3NidXQQ6pvU7xbwiNayzU/7IhvFMweUk2T9hEHp2Kl6iAQC9orMIgpop+Mbcbw+TW2ZcoM3v+6cG4Xgp3v2WdHCycyHXlCPHwbSqHoZ6akhgD9WtrNj1ScGbwJNxjp1HKnixc/ISakEYfdk6n6zZVXr9F0PYVfK15Qe/pR82L/PHoOGAnZ2FWzRCs57xEEAT/mSmxCSFZt3tbfCZJGPPBMvzeHE5sIxX72GQw/DAqnqYaZgi5rQyvk9+kQ2tTp6tZajSld0wbYAKmAeKXT/Vz350GgMC1vA5ikWGKrZR8YKOzQCasu4+VydzeZkz6bvMWDuGHC09vNbm4BOf0C/M9vqkoUZa9cWnl5lFhSQvP0/PsXSXjr7xfeYzyJKF48fsvgIhxNJpE2lV4VTB5e9i3LwvpEmN44fx9ilgIHDl16+eMNlj59SnnywiacxX4teIRo3TjPCKv3dZMcWKLkuTf7uQRh/IeVuk9eL7BYJwfLt4wagdLhk4HTcTTGfDWpeTnGSIb1Q6qmHJ1RXjhwEAsVh5dDTzi0Ud7Vqit/nUogKP84uK0r03uy6ObulA14biUPdNRC97VZTDe8cRspCK6PeaVG1IWHMTIlQvFU5Y7hyk0QzCKaBkKO0LQ7IlIuv7br/+ARlnA==
