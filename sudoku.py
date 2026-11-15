import random
import copy
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd

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


def draw_sudoku(ax, grid, title, given=None):
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_aspect("equal")
    ax.axis("off")
    # ax.set_title(title, fontsize=18, pad=12)
 
    # Grid lines: thick around 3x3 boxes, thin otherwise
    for i in range(10):
        lw = 2.5 if i % 3 == 0 else 0.6
        ax.plot([0, 9], [i, i], color="#681010", linewidth=lw)
        ax.plot([i, i], [0, 9], color="#681010", linewidth=lw)

    # Background of the grid itself
    ax.add_patch(Rectangle((0, 0), 9, 9, facecolor="#dfe9dc", zorder=0))

    # Background of the whole page
    # ax.figure.patch.set_facecolor("#ead1dc")
 
    # Numbers: given digits in bold black, solved digits in blue
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                is_given = given is None or given[r][c]
                ax.text(c + 0.5, 8.5 - r, str(v), ha="center", va="center",
                        fontsize=16, color="black" if is_given else "#332421",
                        # fontsize=16, color="black" if is_given else "tab:blue",
                        fontweight="bold" if is_given else "normal")
 
 
def save_sudoku_pdf(puzzle, solution, title, filename="sudoku.pdf"):
    # size = (8.27, 11.69) # A4
    size = (6,6)
    with PdfPages(filename) as pdf:
        if solution and puzzle:
            for grid, title, given in [(solution, title, puzzle)]:
                fig, ax = plt.subplots(figsize=size)  # A4
                ax = fig.add_axes([0, 0, 1, 1])      # axes cover 100% of the figure
                draw_sudoku(ax, grid, title, given)
                pdf.savefig(fig, transparent=True)
                plt.savefig(title + '.png')
                plt.close(fig)
        else:
            for grid, title, given in [(puzzle, title, None)]:
                fig, ax = plt.subplots(figsize=size)  # A4
                ax = fig.add_axes([0, 0, 1, 1])      # axes cover 100% of the figure
                draw_sudoku(ax, grid, title, given)
                pdf.savefig(fig, transparent=True)
                plt.savefig(title + '.png')
                plt.close(fig)
            # for grid, title, given in [(puzzle, "Puzzle", None),
            #                         (solution, "Solution", puzzle)]:
            #     fig, ax = plt.subplots(figsize=size)  # A4
            #     draw_sudoku(ax, grid, title, given)
            #     pdf.savefig(fig)
            #     plt.close(fig)

def save_sudoku_image(puzzle, filename="sudoku.png"):
    fig, ax = plt.subplots(figsize=(6, 6))
    draw_sudoku(ax, puzzle, title="")
    fig.savefig(filename, bbox_inches="tight", pad_inches=0.05, dpi=200)
    plt.close(fig)

# Hovedprogram
if __name__ == "__main__":

    sudokus = {'sudoku1': 'easy',
            'sudoku2': 'easy',
            'sudoku3': 'easy',
            'sudoku4': 'easy',
            'sudoku5': 'easy',
            'sudoku6': 'easy',
            'sudoku7': 'easy',
            'sudoku8': 'easy',
            'sudoku9': 'easy',
            'sudoku10': 'easy',
            'sudoku11': 'medium',
            'sudoku12': 'medium',
            'sudoku13': 'medium',
            'sudoku14': 'medium',
            'sudoku15': 'medium',
            'sudoku16': 'medium',
            'sudoku17': 'medium',
            'sudoku18': 'medium',
            'sudoku19': 'medium',
            'sudoku20': 'medium',
            'sudoku21': 'hard',
            'sudoku22': 'hard',
            'sudoku23': 'hard',
            'sudoku24': 'hard',
            'sudoku25': 'hard',
            'sudoku26': 'hard',
            'sudoku27': 'hard',
            'sudoku28': 'hard',
            'sudoku29': 'hard',
            'sudoku30': 'hard',
            }
    for key, value in sudokus.items():
        # print(key, value)
        title = key
        difficulty = value
        # difficulty = 'hard'
        # title = 'sudoku1_' + difficulty
        title_solution = title + '_solution_' + difficulty
        full_board = generate_full_board()
        puzzle_board = remove_cells(full_board, difficulty=difficulty)

        df = pd.DataFrame(puzzle_board)
        df.to_csv(title + '.csv')

        pd.DataFrame(puzzle_board).to_csv(title + '.csv')
        
        pd.DataFrame(full_board).to_csv(title_solution + '.csv')

        save_sudoku_pdf(puzzle_board, None, '', title + '.pdf')
        save_sudoku_pdf(puzzle_board, full_board, '', title_solution + '.pdf')
    
    
    
    # save_sudoku_pdf(puzzle_board, full_board, "sudoku_solution.pdf")

    # print("Sudoku: " + difficulty)
    # print_board(puzzle_board)

    # print("Solution:")
    # print_board(full_board)

    # print("Latex format:")
    # print_latex_format(puzzle_board)

    # print("Latex format solution:")
    # print_latex_format(full_board)

    # print("Latex format answers:")
    # print_latex_format_answers(puzzle_board, full_board)
