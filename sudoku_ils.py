import random

Grid = list[list[int]]
def build_grid(numbers: list[int]) -> Grid:
    if len(numbers) != 81:
        raise ValueError(f"Expected 81 numbers, got {len(numbers)}")
    return [numbers[i * 9:(i+1) * 9] for i in range(9)]

def read_puzzles(path: str) -> list[Grid]:
    puzzles: list[Grid] = []
    numbers: list[int] = []

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line :
                continue
            if line.startswith("Grid"):
                if numbers:
                    puzzles.append(build_grid(numbers))
                    numbers= []
            else:
                parts = line.split()
                for p in parts:
                    numbers.append(int(p))
        if numbers: 
            puzzles.append(build_grid(numbers))
    return puzzles 

def print_grid(grid:Grid) -> None:
    for r in range(9):
        row = grid[r]
        line = " ".join(str(x) if x != 0 else "." for x in row)
        print(line)

def get_fixed_cells(grid: Grid) -> list[list[bool]]:
    fixed = [[ False for _ in range(9) ] for _ in range(9)]
    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                fixed[r][c] = True
    return fixed

def generate_start_state(grid: Grid, fixed: list[list[bool]]) -> Grid:
    new_grid: Grid = [row.copy() for row in grid]

    for block_row in range(3):
        for block_col in range(3):
            present = set()
            for r in range(block_row * 3, block_row * 3 + 3 ):
                for c in range(block_col *3, block_col * 3 + 3):
                    if fixed[r][c] and new_grid[r][c]!= 0 :
                        present.add(new_grid[r][c])
            
            remaining = [d for d in range (1, 10) if d not in present]
            random.shuffle(remaining)

            idx = 0 
            for r in range(block_row * 3, block_row * 3 + 3 ):
                for c in range(block_col * 3 , block_col * 3 + 3 ):
                    if not fixed[r][c]:
                        new_grid[r][c] = remaining[idx]
                        idx += 1
    return new_grid

def evaluate(grid:Grid)-> int:
    score = 0
    target = set(range(1, 10 ))

    for r in range(9):
        row_numbers = set(grid[r])
        missing = target - row_numbers
        score += len(missing)

    for c in range(9):
        col_numbers = set(grid[r][c] for r in range(9))
        missing = target - col_numbers
        score += len(missing)
    return score

def get_block_cells(block_row: int, block_col: int):
    cells = []
    for r in range(block_row * 3, block_row * 3 + 3):
        for c in range(block_col * 3, block_col * 3 + 3):
            cells.append((r, c))
    return cells


def generate_swaps(grid: Grid, fixed: list[list[bool]], block_row: int, block_col: int):
    cells = get_block_cells(block_row, block_col)
    free_cells = [(r, c) for (r, c) in cells if not fixed[r][c]]

    swaps = []
    for i in range(len(free_cells)):
        for j in range(i+1, len(free_cells)):
            swaps.append((free_cells[i], free_cells[j]))
    return swaps


def apply_swap(grid: Grid, pos1: tuple[int, int], pos2: tuple[int, int]) -> Grid:
    new_grid = [row.copy() for row in grid]
    r1, c1 = pos1
    r2, c2 = pos2
    new_grid[r1][c1], new_grid[r2][c2] = new_grid[r2][c2], new_grid[r1][c1]
    return new_grid

def hill_climb_step(grid: Grid, fixed: list[list[bool]]):
    current_score = evaluate(grid)

    #Kies willekeurig 1 block
    block_row = random.randint(0, 2)
    block_col = random.randint(0, 2)

    swaps = generate_swaps(grid, fixed, block_row, block_col)
    best_grid = grid
    best_score = current_score

   
    for (p1, p2) in swaps:
        new_grid = apply_swap(grid, p1, p2)
        new_score = evaluate(new_grid)

        #Neem beste uitkomst
        if new_score <= best_score:
            best_score = new_score
            best_grid = new_grid

    improved = best_score < current_score
    return best_grid, best_score, improved

def random_walk(grid: Grid, fixed: list[list[bool]], S: int) -> Grid:
    for _ in range(S):
        block_row = random.randint(0, 2)
        block_col = random.randint(0, 2)
        swaps = generate_swaps(grid, fixed, block_row, block_col)
        if swaps:
            pos1, pos2 = random.choice(swaps)
            grid = apply_swap(grid, pos1, pos2)
    return grid


def iterated_local_search(start_grid: Grid, fixed: list[list[bool]], S: int,
                          max_iters=10000):

    grid = start_grid
    score = evaluate(grid)

    for iteration in range(max_iters):

        # HillClimbing
        improved = True
        while improved and score > 0:
            grid, new_score, improved = hill_climb_step(grid, fixed)
            score = new_score

        if score == 0:
            print("Sudoku opgelost!")
            return grid

        #Geen verbetering, doe random walk
        grid = random_walk(grid, fixed, S)
        score = evaluate(grid)

    print("Max iteraties bereikt.")
    return grid

if __name__ == "__main__":
    puzzles = read_puzzles("./Sudoku_puzzels_5.txt")
    first = puzzles[0]

    fixed = get_fixed_cells(first)
    start = generate_start_state(first, fixed)

    print("Start score:", evaluate(start))

    solved = iterated_local_search(start, fixed, S=10)

    print("\nOplossing:")
    print_grid(solved)
    print("\nEindscore:", evaluate(solved))