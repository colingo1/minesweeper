import random
class Square:
	def __init__(self):
		self.clicked = False
		self.mine = False
		self.flagged = False
		self.num = -1
		self.flags_adjacent = 0
		self.confirmed_mine = False
		self.done = False
		self.hinted = False
		self.possible_mine = False


class Board:
	def __init__(self,rows,cols):
		self.board = []
		self.rows = rows
		self.cols = cols
		self.num_clicked = 0
		self.mine_count = 0
		for y in range(rows):
			row = []
			for x in range(cols):
				row.append(Square())
			self.board.append(row)
	def get_adjacent(self,square_y,square_x):
		adj = []
		for y in range(square_y-1,square_y+2):
				for x in range(square_x-1,square_x+2):
					if y >=0 and x>=0 and y < self.rows and x < self.cols and not (square_y== y and square_x==x):
						adj.append((y,x))
		return adj
	def mines_adjacent(self,square_y,square_x):
		count = 0
		for y in range(square_y-1,square_y+2):
			for x in range(square_x-1,square_x+2):
				if y >=0 and x>=0 and y < self.rows and x < self.cols and not (square_y== y and square_x==x):
					if self.board[y][x].mine:
						count += 1
		return count

	def flags_adjacent(self,square_y,square_x):
		count = 0
		for y in range(square_y-1,square_y+2):
			for x in range(square_x-1,square_x+2):
				if y >=0 and x>=0 and y < self.rows and x < self.cols and not (square_y== y and square_x==x):
					if self.board[y][x].flagged:
						count += 1
		return count

	def generate_board(self, num_mines, starting_y, starting_x):
		self.mine_count=num_mines
		for i in range(num_mines):
			placed = False
			while not placed:
				x = random.randint(0,self.cols-1)
				y = random.randint(0,self.rows-1)
				if((abs(x-starting_x) < 2 and abs(y-starting_y) < 2) or self.board[y][x].mine):
					continue
				self.board[y][x].mine = True
				placed = True
		for y in range(self.rows):
			for x in range(self.cols):
				self.board[y][x].num = self.mines_adjacent(y,x)


	def print_board(self):
		for y in range(self.cols):
			for x in range(self.rows):
				if(self.board[y][x].mine):
					print("X",end="")
				else:
					print(self.board[y][x].num,end="")
			print("")

class partialBoard:
	def __init__(self,full_board):
		self.ref_board = full_board
		self.partialBoard = []
		self.rows = full_board.rows
		self.cols = full_board.cols
		self.board = []
		for y in range(self.rows):
			row = []
			for x in range(self.cols):
				row.append(Square())
				row[x].clicked = self.ref_board.board[y][x].clicked
				row[x].flagged = self.ref_board.board[y][x].flagged
				row[x].confirmed_mine = self.ref_board.board[y][x].confirmed_mine
				row[x].done = self.ref_board.board[y][x].done
				if self.ref_board.board[y][x].clicked:
					row[x].num = self.ref_board.board[y][x].num
			self.board.append(row)

	def num_confirmed_mines(self):
		num_confirmed = 0
		for y in range(self.rows):
			for x in range(self.cols):
				if self.board[y][x].confirmed_mine:
					num_confirmed+=1
		return num_confirmed

	def possible_mines_adjacent(self,square_y,square_x):
		count = 0
		for y in range(square_y-1,square_y+2):
			for x in range(square_x-1,square_x+2):
				if y >=0 and x>=0 and y < self.rows and x < self.cols and not (square_y== y and square_x==x):
					if self.board[y][x].possible_mine:
						count += 1
		return count
	def confirmed_mines_adjacent(self,square_y,square_x):
		count = 0
		for y in range(square_y-1,square_y+2):
			for x in range(square_x-1,square_x+2):
				if y >=0 and x>=0 and y < self.rows and x < self.cols and not (square_y== y and square_x==x):
					if self.board[y][x].confirmed_mine:
						count += 1
		return count
	def verify_partial(self,border_squares, num_confirmed):
		num_possible = 0
		for y,x in border_squares:
			if self.board[y][x].possible_mine:
				num_possible+=1
			for i,j in self.ref_board.get_adjacent(y,x):
				if self.board[i][j].clicked and self.possible_mines_adjacent(i,j)+self.confirmed_mines_adjacent(i,j) != self.board[i][j].num:
					return False
		if num_possible+num_confirmed > self.ref_board.mine_count:
			return False
		return True

	def step(self):
		#First we check for the obvious ones, that have just one step possible
		for y in range(self.rows):
			for x in range(self.cols):
				if self.board[y][x].clicked and not self.board[y][x].done:
					if self.board[y][x].num == 0:
						self.board[y][x].done = True
						continue
					surrounding_count = 0
					for i,j in self.ref_board.get_adjacent(y,x):
						if not self.board[i][j].clicked:
							surrounding_count+=1
					if surrounding_count == self.board[y][x].num:
						print("Found mine situation for spot:({},{})".format(y,x))
						first_x = -1
						first_y = -1
						for i,j in self.ref_board.get_adjacent(y,x):
							if not self.board[i][j].clicked:
								if first_x == -1 and self.board[i][j].confirmed_mine == False and self.ref_board.board[i][j].hinted == False:
									first_y = i
									first_x = j
									self.board[i][j].confirmed_mine = True
									if self.ref_board.board[i][j].mine == False:
										print("THIS SHOULD DEFINITELY NOT HAPPEN: FALSE POSITIVE MINE AT SPACE ({},{})".format(i,j))
									self.ref_board.board[i][j].confirmed_mine = True
									self.ref_board.board[i][j].hinted = True
						if first_y == -1:
							self.ref_board.board[y][x].done = True
							print("spot ({},{}) now done.".format(y,x))
						else:
							return (True,first_y,first_x)

		print("No new mines, checking new free spaces:")


		for y in range(self.rows):
			for x in range(self.cols):
				if self.board[y][x].clicked and not self.board[y][x].done:
					surrounding_mines = 0
					for i,j in self.ref_board.get_adjacent(y,x):
						if self.board[i][j].confirmed_mine:
							surrounding_mines+=1
					if surrounding_mines== self.board[y][x].num:
						print("Found clear situation for spot:({},{})".format(y,x))
						first_x = -1
						first_y = -1
						for i,j in self.ref_board.get_adjacent(y,x):
							if not self.board[i][j].clicked:
								if first_x == -1 and self.board[i][j].confirmed_mine == False and self.ref_board.board[i][j].hinted == False:
									first_y = i
									first_x = j
									self.ref_board.board[i][j].hinted = True
									if self.ref_board.board[i][j].mine == True:
										print("THIS SHOULD DEFINITELY NOT HAPPEN: FALSE POSITIVE FREE SPACE AT SPACE ({},{})".format(i,j))
						if first_y == -1:
							self.ref_board.board[y][x].done = True
							print("spot ({},{}) now done.".format(y,x))
						else:
							return (False,first_y,first_x)

		print("This didn't work, trying some much more heavyweight algorithms.")
		#The Brute Force Approach
		border_squares = []
		for y in range(self.rows):
			for x in range(self.cols):
				if not self.board[y][x].clicked and not self.board[y][x].confirmed_mine:
					neighboring_space = False
					for i,j in self.ref_board.get_adjacent(y,x):
						if self.board[i][j].clicked:
							neighboring_space = True
					if neighboring_space:
						border_squares.append((y,x))


		print("border squares to check:")		
		print(border_squares)
		total_confirmed = self.num_confirmed_mines()

		num_possibilities = 0
		possible_mines = [0] * len(border_squares)
		for n in range(2**len(border_squares)):
			for i,(y,x) in enumerate(border_squares):
				self.board[y][x].possible_mine = True if n & 1<<i else False
			if self.verify_partial(border_squares,total_confirmed):
				num_possibilities += 1
				for i,(y,x) in enumerate(border_squares):
					if self.board[y][x].possible_mine:
						possible_mines[i] +=1
		print(possible_mines)
		print(num_possibilities)
		for index, num in enumerate(possible_mines):
			if num==num_possibilities:
				self.ref_board.board[border_squares[index][0]][border_squares[index][1]].confirmed_mine = True
				return (True,border_squares[index][0],border_squares[index][1])
			if num==0:
				return (False,border_squares[index][0],border_squares[index][1])
















def get_num_color(num):
	if num==0:
		return "black"
	if num==1:
		return "blue"
	if num == 2:
		return "green"
	if num == 3:
		return "red"
	if num == 4:
		return "purple"
	if num == 5:
		return "maroon"
	if num == 6:
		return "teal"
	if num == 7:
		return "black"
	if num == 8:
		return "grey"

