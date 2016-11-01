A minimax algorithm implementation written in python.

Usage

piece positions denoted by  "[x][y][player]|"

With established board, to search depth of 3:
python connect4.py -b "051|152|251|242|" -d 3

With board set in preset.txt, to search depth of 3:
python connect4.py -d 3

With board set in preset.txt, to default search depth (1):
python connect4.py