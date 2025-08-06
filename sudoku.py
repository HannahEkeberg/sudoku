import random
import copy

def is_valid(board, row, col, num):
    # Check row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False
    return True

def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_full_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve(board)
    return board

def remove_cells(board, difficulty='medium'):
    levels = {
        'easy': 30,     # 30 blanks
        'medium': 45,   # 45 blanks
        'hard': 55      # 55 blanks
    }
    blanks = levels.get(difficulty, 45)
    puzzle = copy.deepcopy(board)
    attempts = 0
    while blanks > 0 and attempts < 100:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            blanks -= 1
        attempts += 1
    return puzzle

def print_board(board):
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(val if val != 0 else ".", end=" ")
        print()

def print_latex_format(board):
    for i, row in enumerate(board):
        row_str = r"\setrow "
        for j, val in enumerate(row):
            cell = f"{{{val}}}" if val != 0 else "{ }"
            row_str += cell
            # Dobbel mellomrom etter 3. og 6. kolonne
            if j in [2, 5]:
                row_str += "  "
        print(row_str)

def print_latex_format_answers(puzzle, full):
    for i in range(9):
        row_str = r"\setrow "
        for j in range(9):
            if puzzle[i][j] == 0:
                # Vis svar-tallet fra løsningen der det mangler i puslespillet
                cell = f"{{{full[i][j]}}}"
            else:
                # Ellers, vis tom rute
                cell = "{ }"
            row_str += cell
            if j in [2, 5]:
                row_str += "  "
        print(row_str)


# Hovedprogram
if __name__ == "__main__":
    difficulty = 'hard'
    full_board = generate_full_board()
    puzzle_board = remove_cells(full_board, difficulty=difficulty)

    print("Sudoku: " + difficulty)
    print_board(puzzle_board)

    print("Solution:")
    print_board(full_board)

    print("Latex format:")
    print_latex_format(puzzle_board)

    print("Latex format solution:")
    print_latex_format(full_board)

    print("Latex format answers:")
    print_latex_format_answers(puzzle_board, full_board)
