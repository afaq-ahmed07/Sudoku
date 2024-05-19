# Sudoku Puzzle Solver

## Overview

This project is a Sudoku puzzle solver implemented in Python. The solver uses either the Backtracking algorithm or the AC-3 (Arc-Consistency 3) algorithm to find solutions to Sudoku puzzles. The graphical user interface (GUI) for the application is built using Tkinter.

## Features

- **Sudoku Solver Algorithms**: 
  - **Backtracking Algorithm**: A classic depth-first search algorithm for solving constraint satisfaction problems.
  - **AC-3 Algorithm**: An algorithm used for making a problem arc-consistent.
- **GUI**: A user-friendly interface built with Tkinter.
- **Load Puzzle**: Allows users to input Sudoku puzzles manually.
- **Solve Puzzle**: Automatically solves the input puzzle using the selected algorithm.
- **Clear Puzzle**: Clears the board for new input.

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- Optionally, any additional libraries for enhanced functionality (e.g., NumPy, though it's not strictly necessary for basic functionality).

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/Sudoku.git
    cd Sudoku
    ```

2. **Install required dependencies:**

    Tkinter is included with Python standard libraries, but ensure you have it:

    ```sh
    sudo apt-get install python3-tk  # for Debian/Ubuntu
    sudo yum install python3-tkinter  # for Fedora/RedHat
    ```

3. **Run the application:**

    ```sh
    python3 sudoku.py
    ```

## Usage

1. **Open the application:**

    Run the `sudoku.py` file to start the GUI.

2. **Solve the puzzle:**

    - Click the "Solve" button to solve the puzzle using the selected algorithm.
    - Choose between Backtracking or AC-3 from the options if available.

3. **Clear the puzzle:**

    - Click the "Reset" button to reset the grid for a new puzzle input.
