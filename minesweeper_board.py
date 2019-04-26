from tkinter import *
from minesweeper import *
from functools import partial
import time

disp_board = None
button_arr = None
game_started = False
board = None

def display_board():
	arr = []
	for y in range(rows):
		row = []
		for x in range(cols):
			square = Button(disp_board,text = " ", height = 2, width = 4, bg="#E0E0E0")
			square.bind('<Button-1>', lambda a, x = x, y = y: click_square(a,y,x))
			square.bind('<Button-2>', lambda a, x = x, y = y: print_square(a,y,x))
			square.bind('<Button-3>', lambda a, x  = x, y = y: right_click_square(a,y,x))
			square.grid(column = x, row = y)
			row.append(square)
		arr.append(row)
	global board
	board = Board(rows,cols)
	return arr



def new_game():
	global game_started
	game_started = False
	global disp_board
	disp_board.destroy()
	disp_board = Frame(window)
	global board
	board = None
	global button_arr
	global cols
	cols = setting_cols;
	global rows
	rows = setting_rows;
	global mine_count
	mine_count = setting_mine_count
	button_arr = display_board()
	disp_board.pack()
	global num_flagged
	num_flagged = 0
	num_mines.config(text = str(mine_count-num_flagged))

def modify_board_options(rows_box,cols_box,mines_box):
	global setting_rows
	setting_rows = int(rows_box.get())
	global setting_cols
	setting_cols = int(cols_box.get())
	global setting_mine_count
	setting_mine_count = int(mines_box.get())
	rows_box.master.destroy()


def popup_options_menu():
	popup = Tk()
	popup.title("Board Options")
	rows_box = Entry(popup)
	rows_box.pack()
	cols_box = Entry(popup)
	cols_box.pack()
	mines_box = Entry(popup)
	mines_box.pack()
	confirm_button = Button(popup, text = "Confirm", command = lambda: modify_board_options(rows_box,cols_box,mines_box))
	confirm_button.pack()



def lose_game():
	for row in button_arr:
		for button in row:
			button.config(state = "disabled")

def win_game():
	popup = Tk()
	popup.title("!")
	label = Label(popup, text="You Win!")
	label.pack(side="top", fill="x", pady=10)
	popup.mainloop()

def click_square(event,square_y,square_x):
	global game_started
	if not game_started:
		board.generate_board(mine_count,square_y,square_x)
		game_started = True
	if board.board[square_y][square_x].clicked:
		flags = board.flags_adjacent(square_y,square_x)
		if flags == board.board[square_y][square_x].num:
			for y in range(square_y-1,square_y+2):
				for x in range(square_x-1,square_x+2):
					if y >=0 and x>=0 and y < board.rows and x < board.cols and not (square_y== y and square_x==x):
						if not board.board[y][x].clicked and not board.board[y][x].flagged:
							explore_square(y,x)

	else:
		if not board.board[square_y][square_x].flagged:
			return explore_square(square_y,square_x)

def explore_square(square_y,square_x):
	board.board[square_y][square_x].clicked = True;
	board.num_clicked += 1
	button_arr[square_y][square_x].config(bg="#aaaaaa")
	if board.board[square_y][square_x].mine:
		lose_game()
	else:
		num = board.board[square_y][square_x].num
		button_arr[square_y][square_x].config(fg = get_num_color(num))
		if num != 0:
			button_arr[square_y][square_x].config(text = str(num))
		else:
			for (y,x) in board.get_adjacent(square_y,square_x):
						if not board.board[y][x].clicked:
							explore_square(y,x)
		if board.num_clicked == rows * cols -mine_count:
			win_game()
			return "WIN"
def print_square(event, y,x):
	print("Square ({},{})".format(y,x))
def right_click_square(event, square_y,square_x):
	print(square_y)
	print(square_x)
	global num_flagged
	if not board.board[square_y][square_x].clicked:
		if not board.board[square_y][square_x].flagged:
			button_arr[square_y][square_x].config(text = "F")
			board.board[square_y][square_x].flagged = True;
			num_flagged += 1
			button_arr[square_y][square_x].config(bg="#E0E0E0")
			num_mines.config(text = str(mine_count-num_flagged))
		else:
			button_arr[square_y][square_x].config(text = " ")
			board.board[square_y][square_x].flagged = False;
			num_flagged -= 1
			button_arr[square_y][square_x].config(bg="#E0E0E0")
			num_mines.config(text = str(mine_count-num_flagged))
setting_cols = 8;
setting_rows = 8;
setting_mine_count = 10
cols = setting_cols;
rows = setting_rows;
mine_count = setting_mine_count
num_flagged = 0

def solve_board():
	partial = partialBoard(board)
	move = partial.step()
	if move == None:
		print("Unable to find another move")
		return
	is_mine,y,x = move
	print(move)
	if is_mine:
		right_click_square(0,y,x)
	else:
		ret = click_square(0,y,x)
		if ret== "WIN":
			return
	delay = 10
	if solver_slowmode.get():
		delay = 500
	window.after(delay,solve_board)

def give_hint():
	partial = partialBoard(board)
	hint = partial.step()
	if hint == None:
		print("No Hint available!")
		return
	is_mine,y,x = hint
	print(hint)
	if is_mine:
		print("Square ({},{}) is a mine!".format(y,x))
		if board.board[y][x].flagged:
			give_hint()
		else:
			button_arr[y][x].config(bg = "red")
	else:
		print("Square ({},{}) is safe.".format(y,x))
		button_arr[y][x].config(bg = "green")

def key_press(event):
	if event.char == "h":
		give_hint()
	if event.char == "n":
		new_game()
	if event.char == "s":
		solve_board()
window = Tk()
disp_board = Frame(window)
window.title("Minesweeper")
menu = Menu(window)
submenu = Menu(menu,tearoff = 0)
submenu.add_command(label = "New", command = new_game)
#submenu.add_command(label = "Close",command = )
#submenu.add_command(label = "Restart")
#submenu.add_command(label = "Load")

board_menu = Menu(menu,tearoff = 0)
board_menu.add_command(label = "Board Settings", command = popup_options_menu)
board_menu.add_command(label = "Get Hint", command = give_hint)
board_menu.add_command(label = "Solve Board", command = solve_board)
solver_slowmode = BooleanVar()
solver_slowmode.set(True)
board_menu.add_checkbutton(label="Slow Solve", onvalue=1, offvalue=False, variable=solver_slowmode)


#board_menu.add_command(label = "Mark Unsolvable")
menu.add_cascade(label = "Menu",menu = submenu)
menu.add_cascade(label = "Board",menu = board_menu)
window.config(menu=menu)

button_arr = display_board()
num_mines = Label(window,text = str(mine_count))
num_mines.pack()
disp_board.pack()




window.bind("<Key>", key_press)
window.mainloop()

