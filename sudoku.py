import tkinter as tk
import customtkinter as ctk
import time

BOARDS = ['Puzzle 1', 'Puzzle 2']

WIDTH = 540
HEIGHT = 540
MARGIN = 20
SIDE = (WIDTH - 2 * MARGIN) / 9


class SudokuError(Exception):
    pass


class Sudoku:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku")
        self.root.geometry('800x600')

        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)

        # Initialize the canvas attribute at the class level
        self.canvas = tk.Canvas(self.frame1, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.selected_algorithm = tk.IntVar(value=0)
        self.time = 0
        self.selected_puzzle = tk.IntVar(value=0)
        self.change_list = []

        try:
            with open(f'{"easy1"}.sudoku', 'r') as boards_file:
                self.board = self.create_board(boards_file)
        except FileNotFoundError:
            print(f"No file found for board: {self.board_name}")
        except SudokuError as e:
            print(str(e))

        self.configure_frames()
        self.create_buttons()
        self.create_labels_and_radiobuttons()
        self.display_board()

        self.root.mainloop()

    def configure_frames(self):
        self.frame1.grid(row=0, column=0, sticky="ns")
        self.frame2.grid(row=0, column=1, sticky="ns")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def create_buttons(self):
        solve_button = ctk.CTkButton(self.frame2, text="Reset", width=100, height=100, command=self.reset_puzzle)
        solve_button.pack(padx=5, pady=20)

        reset_button = ctk.CTkButton(self.frame2, text="Solve", width=100, height=100, command=self.solve_puzzle)
        reset_button.pack(padx=5, pady=10)

    def create_labels_and_radiobuttons(self):
        algorithm_label = ctk.CTkLabel(self.frame2, text="Algorithm:", text_color="black")
        algorithm_label.pack(anchor='w', padx=5, pady=10)

        ac3_radio = ctk.CTkRadioButton(self.frame2, text="AC-3", text_color="black", corner_radius=50, value=0,
                                       variable=self.selected_algorithm)
        ac3_radio.pack(anchor='w', padx=10, pady=5)

        backtracking_radio = ctk.CTkRadioButton(self.frame2, text="Backtracking", text_color="black", corner_radius=50,
                                                value=1, variable=self.selected_algorithm)
        backtracking_radio.pack(anchor='w', padx=10, pady=5)

        puzzle_label = ctk.CTkLabel(self.frame2, text="Choose Puzzle:", text_color="black")
        puzzle_label.pack(anchor='w', padx=5, pady=10)

        self.difficulty_menu=ctk.CTkOptionMenu(self.frame2,values=["Easy","Medium","Hard"])
        self.difficulty_menu.pack(padx=5,pady=5)

        count = 0
        for i, board in enumerate(BOARDS):
            checkbox = ctk.CTkRadioButton(self.frame2, text=board, text_color="black", corner_radius=50, value=count,
                                          variable=self.selected_puzzle)
            checkbox.pack(anchor='w', padx=10, pady=5)
            count += 1
        self.time_label = ctk.CTkLabel(self.frame1, text=f"Time: {self.time}", text_color="black")
        self.time_label.pack(anchor='w', padx=5, pady=5, expand=False)

    def create_board(self, board_file):
        board = []
        for line in board_file:
            line = line.strip()
            if len(line) != 9:
                raise SudokuError(
                    "Each line in the sudoku puzzle must be 9 chars long."
                )
            board.append([int(c) for c in line])

        if len(board) != 9:
            raise SudokuError("Each sudoku puzzle must be 9 lines long")
        return board

    def display_board(self):
        self.__draw_grid()
        self.__draw_puzzle(self.board)

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self, puzzle):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                if (i, j) in self.change_list:
                    color = "red"
                else:
                    color = "black"
                answer = puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    self.canvas.create_text(x, y, text=answer, tags="numbers", fill=color)

    def solve_puzzle(self):
        """
        Solves the Sudoku puzzle based on the selected algorithm.
        """
        if self.selected_algorithm.get() == 0:  # AC-3 selected
            self.solve_arc_consistency()
            self.display_board()
        elif self.selected_algorithm.get() == 1:  # Backtracking selected
            self.solve_backtracking()
            self.display_board()

    def select_difficulty(self, difficulty):
        self.select_board(difficulty)
    def select_board(self,difficulty):
        if difficulty=="Easy":
            if self.selected_puzzle.get() == 0:
                self.board_name = "easy1"
            elif self.selected_puzzle.get() == 1:
                self.board_name = "easy2"

        elif difficulty=="Medium":
            if self.selected_puzzle.get() == 0:
                self.board_name = "medium1"
            elif self.selected_puzzle.get() == 1:
                self.board_name = "medium2"
        elif difficulty=="Hard":
            if self.selected_puzzle.get() == 0:
                self.board_name = "hard1"
            elif self.selected_puzzle.get() == 1:
                self.board_name = "hard2"
    def reset_puzzle(self):
        self.select_difficulty(self.difficulty_menu.get())
        try:
            with open(f'{self.board_name}.sudoku', 'r') as boards_file:
                self.board = self.create_board(boards_file)
                self.change_list = []
                self.__draw_grid()
                self.__draw_puzzle(self.board)
        except FileNotFoundError:
            print(f"No file found for board: {self.board_name}")
        except SudokuError as e:
            print(str(e))

    def is_valid(self, board, row, col, num):
        """
        Checks if the number can be placed at the given position.
        """
        # Check the number in the row
        for x in range(9):
            if board[row][x] == num:
                return False

        # Check the number in the column
        for x in range(9):
            if board[x][col] == num:
                return False

        # Check the number in the 3x3 box
        start_row, start_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False

        return True

    def solve(self, board):
        """
        Recursive function to solve the Sudoku board using backtracking.
        """
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    self.change_list.append((i, j))
                    for num in range(1, 10):
                        if self.is_valid(board, i, j, num):
                            board[i][j] = num
                            if self.solve(board):
                                return True
                            board[i][j] = 0
                    return False
        return True

    def solve_backtracking(self):
        """
        Attempts to solve the Sudoku board using backtracking.
        Measures the time taken to solve the puzzle.
        """
        start_time = time.perf_counter()  # Record the start time

        if not self.solve(self.board):
            raise SudokuError("No solution exists for this Sudoku puzzle.")

        end_time = time.perf_counter()  # Record the end time
        self.time = round(end_time - start_time, 5)
        self.time_label.destroy()
        self.time_label = ctk.CTkLabel(self.frame1, text=f"Time: {self.time} seconds", text_color="black")
        self.time_label.pack(anchor='w', padx=5, pady=5, expand=False)

    def get_row(self, board, row):
        return [board[row][col] for col in range(9)]

    def get_column(self, board, col):
        return [board[row][col] for row in range(9)]

    def get_block(self, board, row, col):
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        block = []
        for i in range(3):
            for j in range(3):
                block.append(board[start_row + i][start_col + j])
        return block

    def get_empty_cells(self, board):
        empty_cells = []
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    self.change_list.append((row, col))
                    empty_cells.append((row, col))
        return empty_cells

    def revise_domain(self, board, cell, domain):
        row, col = cell
        revised = False
        for value in list(domain):
            if value in self.get_row(board, row) or value in self.get_column(board, col) or value in self.get_block(
                    board, row,
                    col):
                domain.remove(value)
                revised = True
        return revised

    def apply_arc_consistency(self, board):
        domains = {}
        for row in range(9):
            for col in range(9):
                domains[(row, col)] = set(range(1, 10))
        queue = self.get_empty_cells(board)

        while queue:
            row, col = queue.pop(0)
            if self.revise_domain(board, (row, col), domains[(row, col)]):
                for neighbor in self.get_row(board, row) + self.get_column(board, col) + self.get_block(board, row,
                                                                                               col):
                    if neighbor == 0:
                        continue
                    if self.revise_domain(board, (row, col), domains[(row, col)]):
                        queue.append((row, col))

        for cell in domains:
            if len(domains[cell]) == 1:
                row, col = cell
                board[row][col] = domains[cell].pop()

    def solve_arc_consistency(self):
        start_time = time.perf_counter()  # Record the start time
        # Copy the board to work with a local copy
        board_copy = [row[:] for row in self.board]
        self.apply_arc_consistency(board_copy)
        # Check if the board is solved
        for row in board_copy:
            if 0 in row:
                raise SudokuError("No solution exists for this Sudoku puzzle.")
        # Update the original board with the solved values
        self.board = board_copy
        end_time = time.perf_counter()  # Record the end time
        self.time = round(end_time - start_time, 5)
        self.time_label.destroy()
        self.time_label = ctk.CTkLabel(self.frame1, text=f"Time: {self.time} seconds", text_color="black")
        self.time_label.pack(anchor='w', padx=5, pady=5, expand=False)


if __name__ == "__main__":
    app = Sudoku()
