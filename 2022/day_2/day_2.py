def score_round(op_play: str, your_play: str) -> int:
	if (
		(op_play == "A" and your_play == "B") or 
		(op_play == "B" and your_play == "C") or 
		(op_play == "C" and your_play == "A")
		):
		return 6
	if op_play == your_play:
		return 3
	else:
		return 0


def score_shape(play: str) -> int:
	match play:
		case "A":
			return 1
		case "B":
			return 2
		case "C":
			return 3


filename = "input.txt"
game_score = []

with open(filename, "r") as f:
	for line in f:
		line = line.strip()

		op_play = line[0]
		your_play = chr(ord(line[2]) - 23)	# shifting your character to mathc your oponement, i.e "X" becomes "A"

		game_score.append(score_round(op_play, your_play) + score_shape(your_play))

print(sum(game_score))
