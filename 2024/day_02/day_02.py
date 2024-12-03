from __future__ import annotations

import itertools as it
import sys
print(sys.executable)


def check_safe(report: list, dampener: bool, verbose: bool=True) -> bool:
	# print(f"{report} checking")
	safe = True
	level_i = None
	distances = []
	for level_grp, level_idx in zip(it.pairwise(report), it.pairwise(list(range(len(report))))):
		
		dist = level_grp[0] - level_grp[1]
		# print(level_grp, dist)
		distances.append(dist)

		if not(1 <= abs(dist) <= 3):
			# print("adj not passed")
			safe = False

		if len(distances) != 0:
			# print(f"{distances = }")
			if min(distances) < 0 < max(distances): # not same sign test
				safe = False

	if not safe and dampener:
		for level_i in range(len(report)):
			report_dampened = report.copy()
			report_dampened.pop(level_i)

			safe = check_safe(report_dampened, dampener=False, verbose=False)
			if safe:
				break

	if verbose:
		pprint(report, safe, level_i)
	return safe # not errors cause counting the passes, ie. ¬ errors


def analyse_reports(lines: lines, dampener: bool):
	safe_reports = []

	for i, line in enumerate(lines):
		report = list(map(int, line.split()))
		print(i, end="\t")

		if check_safe(report, dampener):
			safe_reports.append(safe_reports)

	return len(safe_reports)


def pprint(report, safe, dampened_idx):
	if safe:
		check = "\033[92m V\033[0m"
	else:
		check = "\033[91m X\033[0m"

	report_str = ""
	for i, s in enumerate(report):
		if dampened_idx == i and safe:
			report_str += f"\033[91m{s}\033[0m"
		else:
			report_str += str(s)
		report_str += " "


	print(f"{check} {report_str}")


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	result_1 = analyse_reports(lines, dampener=False)
	
	result_2 = analyse_reports(lines, dampener=True)
	
	print(f"Part I: {result_1}")
	print("=====\n")
	print(f"Part II: {result_2}")


if __name__ == "__main__":
	main()
