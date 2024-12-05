from __future__ import annotations


def correct_wrong_updates(wrong_updates, rules):
	corrected_updates = []

	for u in wrong_updates:
		rules_to_check = rules.copy()
		c_updates = u.copy()

		while rules_to_check:
			r = rules_to_check.pop(0)

			if r[0] in c_updates and r[1] in c_updates:
				first_page = c_updates.index(r[0])
				second_page = c_updates.index(r[1])

				if second_page < first_page:
					# swap pages - restart checking all rules.
					rules_to_check = rules.copy()

					c_updates[first_page], c_updates[second_page] = c_updates[second_page], c_updates[first_page]

		if c_updates:
			corrected_updates.append(c_updates)

	return corrected_updates


def find_correct_updates(updates, rules):
	correct_updates = []
	wrong_updates = []

	for upd in updates:
		rules_passed = []

		for r in rules:
			if r[0] in upd:
				first_page = upd.index(r[0])

				if r[1] in upd:
					second_page = upd.index(r[1])
					if second_page > first_page:
						rules_passed.append(r)
				else:
					rules_passed.append(r)
			else:
				rules_passed.append(r)
		
		if len(rules_passed) == len(rules):
			correct_updates.append(upd)
		else:
			wrong_updates.append(upd)

	return correct_updates, wrong_updates


def get_middle_pages(updates):
	middle_pages = []
	for u in updates:
		middle_pages.append(u[len(u) // 2])
	return middle_pages


def parse(lines) -> tuple[list[tuple[int, int]], list[list]]:
	s = lines.index("")
	rules = lines[:s]
	updates = lines[s+1:]

	rules = [tuple(map(int, r.split("|"))) for r in rules]
	updates = [list(map(int, u.split(","))) for u in updates]
	
	return rules, updates


def main() -> None:
	filename = "input.txt"

	with open(filename, "r") as f:
		lines = [line.strip() for line in f]

	rules, updates = parse(lines)
	correct_updates, wrong_updates = find_correct_updates(updates, rules)

	middle_pages = get_middle_pages(correct_updates)

	print(f"Part I: {sum(middle_pages)}")

	corrected_updates = correct_wrong_updates(wrong_updates, rules)
	middle_corrected_pages = get_middle_pages(corrected_updates)
	print(f"Part II: {sum(middle_corrected_pages)}")


if __name__ == "__main__":
	main()
