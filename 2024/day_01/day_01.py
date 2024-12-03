from __future__ import annotations


def find_distance(lines: list) -> int:
	lh_lst = []
	rh_lst = []
	for line in lines:
		lh, rh = line.split()
		
		lh_lst.append(int(lh))
		rh_lst.append(int(rh))

	lh_lst.sort()
	rh_lst.sort()

	distances = []
	for lh, rh in zip(lh_lst, rh_lst):
		distance = abs(lh - rh)
		distances.append(distance)

	return sum(distances)


def find_similarity(lines: list) -> int:
	lh_lst = []
	rh_lst = []
	for line in lines:
		lh, rh = line.split()
		
		lh_lst.append(int(lh))
		rh_lst.append(int(rh))

	similarities = []
	for lh in lh_lst:
		occ = rh_lst.count(lh)
		sim = lh * occ
		similarities.append(sim)

	return sum(similarities)


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	result_1 = find_distance(lines)
	print(f"Part I: {result_1}")

	result_2 = find_similarity(lines)
	print(f"Part II: {result_2}")




if __name__ == "__main__":
	main()
