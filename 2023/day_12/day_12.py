from __future__ import annotations

import functools

@functools.lru_cache(maxsize=None)
def count_record(record: str, group: tuple[int]) -> int:
	# print(record, group)

	if not group:
		if "#" not in record:
			# no more damaged spring that would be counted in group
			return 1
		else:
			# only "." so no more arrangement possible
			return 0

	elif not record:
		# record still no springs but still more groups
		return 0

	current_spring = record[0]
	current_group = group[0]

	def dot():
		# don't care if it is a dot, only # counts in groups
		return count_record(record[1:], group)

	def pound():
		# if start with #, then the first n (n=current_group) must be #
		spring_group = record[:current_group]
		spring_group = spring_group.replace("?", "#")

		# check if the spring group is actually all # (no .),
		# it will obviously be the same size
		if spring_group != current_group * "#":
			return 0

		# if the nbr of spring left is the same as the current group,
		# then only one arrangement possible
		if len(record) == current_group:
			# check if last group
			if len(group) == 1:
				return 1
			else:
				# no more groups
				return 0

		# Making sure the next char is a group separator, i.e. "?" or "."
		if record[current_group] in "?.":
			return count_record(record[current_group+1:], group[1:])

		return 0

	if current_spring == ".":
		total = dot()

	elif current_spring == "#":
		total = pound()

	elif current_spring == "?":
		# branch out for both possibilities
		total = dot() + pound()

	return total 



def count_springs(records: list[tuple[str, tuple[int]]]) -> int:
	total = 0
	for record, group in records:
		arr = count_record(record, group)
		total += arr

	return total


def parse_lines(lines: list) -> list[tuple[str, tuple[int]]]:
	records = []
	for line in lines:
		springs, nbr = line.split()
		nbr = tuple(map(int, nbr.split(",")))

		records.append((springs, nbr))
	return records


def unfold_records(records: list[tuple[str, tuple[int]]]) -> list[tuple[str, tuple[int]]]:
	unfolded_records = []
	for springs, group in records:
		unfolded_spring = springs
		unfolded_group = group * 5

		for i in range(4):
			unfolded_spring += f"?{springs}"

		unfolded_records.append((unfolded_spring, unfolded_group))

	return unfolded_records


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	records = parse_lines(lines)
	result1 = count_springs(records)

	records_2 = unfold_records(records)
	result2 = count_springs(records_2)

	print(f"Part I: {result1}")
	print(f"Part II: {result2}")


if __name__ == "__main__":
	main()
