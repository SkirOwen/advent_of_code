from __future__ import annotations


def turn_battery(battery, nbr=2):

	start = 0
	jolt = 0

	for n in range(nbr):

		if n == nbr-1:
			end = None
		else:
			end = -(nbr - 1) + n 

		new_battery = battery[start:end]
		print(new_battery)


		idx = new_battery.index(max(new_battery))
		value = new_battery[idx]

		start += idx+1

		jolt += value * 10 ** (nbr-1 - n)


	print(f"{jolt = }")
	print("--")

	return jolt




def total_jolt(batteries, nbr=2):
	total = []
	for battery in batteries:
		jolt = turn_battery(battery, nbr)
		total.append(jolt)

	return total




def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [list(map(int, line.strip())) for line in f]


	jolt_2 = total_jolt(lines, nbr=2)
	print(sum(jolt_2))

	jolt_12 = total_jolt(lines, nbr=12)
	print(sum(jolt_12))


if __name__ == "__main__":
	main()
