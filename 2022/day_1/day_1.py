

filename = "input.txt"
calorie_counter_per_elf = 0
calorie_per_elf = []

with open(filename, "r") as f:
	for line in f:
		if line == "\n":
			calorie_per_elf.append(calorie_counter_per_elf)
			calorie_counter_per_elf = 0
		else:
			calorie_counter_per_elf += int(line.strip())

print(f"{max(calorie_per_elf) = }")

# part two

nbr_top_elves = 3 	# Number of top elves to selected

sorted_calorie_per_elf = sorted(calorie_per_elf, reverse=True)
print(f"{sum(sorted_calorie_per_elf[:nbr_top_elves]) = }")
