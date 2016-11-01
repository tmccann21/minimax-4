import sys
from optparse import OptionParser
from copy import deepcopy
import random

def parseBoard(board):
	lob = [0] * (7*6);
	pieces = board.split("|")
	for p in pieces:
		if(len(p) == 3): 
			x = int(p[0])
			y = int(p[1])
			t = int(p[2])
			lob[y*7+x] = t
	return lob

class board(object):
	def __init__(self, board):
		self.board = board

	def showBoard(self):
		print("---------")
		for y in range(0,6):
			ln = "|"
			for x in range(0,7):
				ln+=str(self.board[y*7+x])
			print(ln+"|")
		print("---------")

	def makeMove(self, c, p):
		if(self.board[c] == 0):
			for y in range(0,6):
				if(self.board[(5-y)*7+c] == 0):
					self.board[(5-y)*7+c] = p
					break

	def scoreBoard(self, c):
		return self.countStreaks(c, 2) + self.countStreaks(c, 3) * 10 + self.countStreaks(c, 4) * 1000

	def countStreaks(self, c, s):
		count = 0
		for y in range(0,6):
			for x in range(0,7):
				count += self.verticalStreak(x, y, c, s)
				count += self.horizontalStreak(x, y, c, s)
				count += self.diagonalStreak(x, y, c, s)

		return count

	def verticalStreak(self, x, y, c, s):
		cons = 0
		for i in range(y, 6):
			if (self.board[i*7+x] == c):
				cons += 1
			else:
				break
		if cons >= s:
			return 1
		else:	
			return 0
    
	def horizontalStreak(self, x, y, c, s):
		cons = 0
		for i in range(x, 7):
			if (self.board[y*7+i] == c):
				cons += 1
			else:
				break

		if cons >= s:
			return 1
		else:
			return 0

	def diagonalStreak(self, x, y, c, s):

		total = 0
		cons = 0
		j = x
		for i in range(y, 6):
			if j > 6:
				break
			elif (self.board[i*7+j] == c):
				cons += 1
			else:
				break
			j += 1
            
		if cons >= s:
			total += 1
 
		cons = 0
		j = x
		for i in range(y, -1, -1):
			if j > 6:
				break
			elif (self.board[i*7+j] == c):
				cons += 1
			else:
				break
			j += 1

		if cons >= s:
			total += 1

		return total

	def getBoard(self):
		return self.board


class connect4(object):
	def __init__(self):
		self.info = "Pyton connect 4 move analyzer"
		self.depth = 1

	def minimax(self,currentBoard,d,p):
		bestAlpha = -999999
		bestMoves = []
		for i in range(0,7):
			tempBoard = deepcopy(currentBoard)
			if(tempBoard.getBoard()[i] == 0):
				tempBoard.makeMove(i,p)
				alpha = 0
				if(p == 2):
					alpha = tempBoard.scoreBoard(p)
					if(d > 1 and alpha < 1000):
						nextDepth = d-1
						alpha = -self.minimax(tempBoard, nextDepth, 1)['alpha']
				else:
					if(d == 1):
						alpha = tempBoard.scoreBoard(p)
					else:
						nextDepth = d-1
						alpha = self.minimax(tempBoard, nextDepth, 2)['alpha']
				print(alpha)
				if(alpha == bestAlpha):
					bestMoves.insert(0,i)
				elif(alpha > bestAlpha):
					bestMoves = [i]
					bestAlpha=alpha
		return {'moves':bestMoves, 'alpha':bestAlpha}




	def startup(self):
		usage = '%s [-b board state] [-d search depth]' % sys.argv[0]
		optionParser = OptionParser(version = self.info, usage = usage)

		optionParser.add_option('-b',  dest = 'board',              
			help = 'current board state')

		optionParser.add_option('-d',  dest = 'depth',              
			help = 'search depth')

		(options, args) = optionParser.parse_args()

		if not options.board:    
			with open("../preset.txt") as f:
				content = f.readlines()[0]
				self.board = board(parseBoard(content))
		else:
			self.board = board(parseBoard(options.board))

		if options.depth:
			self.depth = int(options.depth)
		else:
			print("No depth given; using d = 1\n")
		print("Initial board state : ")
		self.board.showBoard()
		print("Calculating best move...")
		result = self.minimax(self.board,self.depth,2)
		print(result['moves'])



con4 = connect4()
con4.startup()

