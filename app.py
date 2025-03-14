import time
import turtle
import threading
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from scrape_board_elements import find_grid_values_from_sudoku_webpage

class Board:
    def __init__(self, grid):
        self.grid = grid
        self.updated_cells = []

    def create_checkerboard_design(self, first_color, second_color): # colors must be in rgb
        def create_grid_image(first_color, second_color):
            width, height = 300, 300  
            cell_width = width // 3
            cell_height = height // 3

            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)

            for row in range(3):
                for col in range(3):
                    color = first_color if (row + col) % 2 == 0 else second_color
                    draw.rectangle([col * cell_width, row * cell_height,
                                    (col + 1) * cell_width, (row + 1) * cell_height], fill=color)

            image.save('background_image.jpg')

        def display_background_image():
            background_image = Image.open("background_image.jpg")

            image_width = 474
            image_height = 392 
            background_image = background_image.resize((image_width, image_height), Image.Resampling.LANCZOS)

            background_image = ImageTk.PhotoImage(background_image)

            background_label = tk.Label(self.frame, image=background_image)
            background_label.place(width=image_width, height=image_height)

            background_label.image = background_image

        create_grid_image(first_color, second_color)
        display_background_image()

    def create_board_from_grid(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                cell = self.grid[row][col]
                cell = Cell(cell)
    
    def create_board(self):
        def change_cell_value(row, col, value):
            self.entries[row][col].delete(0, tk.END) 
            self.entries[row][col].insert(0, str(value))
        
        red = (255, 0, 0)  
        blue = (0, 0, 255) 
        self.create_checkerboard_design(red, blue)

        for row in range(9):
            for col in range(9):
                cell = self.grid[row][col]
                entry = tk.Entry(self.frame, width=2, font=("Arial", 18), justify="center", validate="key", validatecommand=(self.validate_command, "%P"))
                entry.grid(row=row, column=col, ipadx=10, ipady=5, padx=(2 if col % 3 == 2 else 1), pady=(2 if row % 3 == 2 else 1))
                self.entries[row][col] = entry
                entry.bind("<FocusOut>", lambda e, r=row, c=col: self.update_cell(r, c))
                if cell.visible:
                    change_cell_value(row, col, cell.value)

    def update_cell(self, row, col):
        if self.entries[row][col].get() == self.grid[row][col].value:
            self.entries[row][col].config(bg="green")
        elif self.entries[row][col].get().strip():
            self.entries[row][col].config(bg="red")

    def initilize_board(self):
        def validate_input(cell):
            return cell == "" or (cell.isdigit() and 1 <= int(cell) <= 9)
        
        def convert_integer_array_to_Cell_array(integer_grid):
            cell_grid = []
            for row in range(9):
                cell_grid_row = []
                for col in range(9):
                    cell = Cell(integer_grid[row][col])
                    cell_grid_row.append(cell)
                cell_grid.append(cell_grid_row)
            return cell_grid

        self.root = tk.Tk()
        self.root.title("Sudoku Board")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.validate_command = self.root.register(validate_input) # restricts the input that can be entered into each cell

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.grid = convert_integer_array_to_Cell_array(self.grid)
        self.find_values_of_cells()
        self.create_board()
                
    def display_board(self): 
        self.create_board()
        self.root.mainloop()

    '''
    Implements a backtracking algorithm to solve a Sudoku board
    '''
    def find_values_of_cells(self): 
        def is_cell_valid(row, col, num):
            # check row cells
            for i in range(9):
                if self.grid[i][col].value == str(num):
                    return False

            # check column cells
            for i in range(9):
                if self.grid[row][i].value == str(num):
                    return False
                
            # check cells in the same square
            top_left_row, top_left_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(3):
                for j in range(3):
                    if self.grid[top_left_row + i][top_left_col + j].value == str(num):
                        return False

            return True
        
        for row in range(9):
            for col in range(9):
                if self.grid[row][col].value == '':                  
                    for num in range(1, 10):
                        if is_cell_valid(row, col, num):
                            self.grid[row][col].value = str(num)
                            if self.find_values_of_cells():
                                return True
                        self.grid[row][col].value = ''
                    return False
        return True
        
class Cell:
    def __init__(self, value):
        self.value = value
        self.visible = True
        if self.value == '':
            self.visible = False
        

'''
AI generated loading icon with Turtle
GUI must be run in the main thread
'''
def loading_icon():
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.title("Loading Icon")
    screen.tracer(0)

    spinner = turtle.Turtle()
    spinner.hideturtle()
    spinner.speed(0)

    colors = ["#E0E0FF", "#C0C0FF", "#8080FF", "#4040FF", "#0000FF", "#4040FF", "#8080FF", "#C0C0FF"]

    stop = False

    def draw_spinner():
        while thread.is_alive():
            spinner.clear()
            for i in range(8):
                spinner.penup()
                spinner.goto(0, 0)
                spinner.setheading(i * 45)
                spinner.forward(50)
                spinner.pendown()
                spinner.dot(10, colors[i])
                spinner.penup()
                spinner.backward(50)
            
            colors.insert(0, colors.pop())
            screen.update()
            time.sleep(0.1)
        screen.bye()
    draw_spinner()

grid = []

thread = threading.Thread(target=find_grid_values_from_sudoku_webpage, args=(grid, )) # must have an extra comma because the args parameter expects a tuple argument
thread.start()

loading_icon()
thread.join()

board = Board(grid)
board.initilize_board()
board.display_board()