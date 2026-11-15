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
    """Samme som hos deg: skriver ut en 9x9-tabell med tall / tomme ruter."""
    for i, row in enumerate(board):
        row_str = r"\setrow "
        for j, val in enumerate(row):
            cell = f"{{{val}}}" if val != 0 else "{ }"
            row_str += cell
            # Dobbel mellomrom etter 3. og 6. kolonne
            if j in [2, 5]:
                row_str += "  "
        print(row_str)

# ========= Killer sudoku: generering av bur =========

def generate_killer_cages(solution_board, min_cage_size=2, max_cage_size=4):
    """
    Lager bur (cages) for killer sudoku:
    - Hvert bur er sammenhengende (4-naboer).
    - Ingen gjentatte tall i samme bur.
    - Summen i buret hentes fra løsningstavlen.
    """
    n = 9
    unassigned = {(r, c) for r in range(n) for c in range(n)}
    cages = []

    while unassigned:
        # Start nytt bur i en tilfeldig celle
        r, c = random.choice(tuple(unassigned))
        cage_cells = [(r, c)]
        unassigned.remove((r, c))
        used_digits = {solution_board[r][c]}

        target_size = random.randint(min_cage_size, max_cage_size)

        while len(cage_cells) < target_size:
            # Finn alle mulige naboer som:
            # - fortsatt er unassigned
            # - har et tall som ikke allerede er i buret
            neighbors = []
            for (cr, cc) in cage_cells:
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < n and 0 <= nc < n and (nr, nc) in unassigned:
                        digit = solution_board[nr][nc]
                        if digit not in used_digits:
                            neighbors.append((nr, nc))

            if not neighbors:
                # Ingen flere lovlige naboer -> avslutt buret tidligere
                break

            nr, nc = random.choice(neighbors)
            cage_cells.append((nr, nc))
            unassigned.remove((nr, nc))
            used_digits.add(solution_board[nr][nc])

        cage_sum = sum(solution_board[r][c] for (r, c) in cage_cells)
        cages.append({"cells": cage_cells, "sum": cage_sum})

    return cages

# ========= Utskrift av killer sudoku =========

def print_killer_grid():
    """
    Skriver ut en tom 9x9-grid for killer sudoku (ingen givens).
    """
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(".", end=" ")
        print()

def print_killer_cages(cages):
    """
    Skriver ut bur: sum + liste med celler (1-basert) i konsollen.
    """
    for i, cage in enumerate(cages):
        cells_str = ", ".join([f"({r+1},{c+1})" for r, c in cage["cells"]])
        print(f"Cage {i+1:2d}: sum = {cage['sum']:2d}  cells = {cells_str}")

def print_latex_killer_grid():
    """
    LaTeX-versjon av tomt 9x9-brett (ingen givens).
    Samme \setrow-struktur som du allerede bruker.
    """
    for i in range(9):
        row_str = r"\setrow "
        for j in range(9):
            cell = "{ }"
            row_str += cell
            if j in [2, 5]:
                row_str += "  "
        print(row_str)

def print_latex_cages(cages):
    """
    Skriver ut bur i et format som kan kobles til LaTeX-makroer.
    Her brukes:
        \killerCage{SUM}{r1c1 r1c2 r2c1}
    Du kan selv definere \killerCage i LaTeX eller tilpasse output-formatet.
    """
    # for i, cage in enumerate(cages):
    #     cell_tokens = [f"r{r+1}c{c+1}" for r, c in cage["cells"]]
    #     cells_str = " ".join(cell_tokens)
    #     print(f"% Cage {i+1}")
    #     print(f"\\killerCage{{{cage['sum']}}}{{{cells_str}}}")

    print(r"\begin{sudoku}")

    for i, cage in enumerate(cages):
        cell_tokens = [f"r{r+1}c{c+1}" for r, c in cage["cells"]]
        cells_str = ",".join(cell_tokens)
        print(f"    % Cage {i+1}")
        print(f"    \\cage{{{cage['sum']}}}{{{cells_str}}}")

    print(r"\end{sudoku}")

# ========= Hovedprogram: killer sudoku =========

if __name__ == "__main__":
    # 1. Generer fullt sudoku-brett (løsning)
    full_board = generate_full_board()

    # 2. Generer killer-bur basert på løsningen
    cages = generate_killer_cages(full_board,
                                  min_cage_size=2,
                                  max_cage_size=4)

    # 3. Skriv ut killer-puslespill (tom grid + bur)
    print("Killer Sudoku (puslespill):")
    print_killer_grid()
    print("\nCages:")
    print_killer_cages(cages)

    # 4. Skriv ut løsning (vanlig brett)
    print("\nLøsning:")
    print_board(full_board)

    # 5. LaTeX-utskrift
    print("\nLaTeX: tomt killer-brett (puslespill):")
    print_latex_killer_grid()

    print("\nLaTeX: løsning (vanlig sudoku-grid):")
    print_latex_format(full_board)

    print("\nLaTeX: bur (bruk i egne killer-makroer):")
    print_latex_cages(cages)


