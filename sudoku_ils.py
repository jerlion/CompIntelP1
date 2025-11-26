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

def evaluatiefunctie(grid: Grid):
    score = 0

    for rij in range (9):
        gemist = 9 - len(set(grid[rij]))
        score = score + gemist

    for kol in range (9):
        kolom = [grid[rij][kol] for rij in range(9)]
        gemist = 9 - len(set(kolom))
        score = score + gemist 
    return score

def krijg_blok(blok_rij: int, blok_kol: int):
    return [
        (rij, kol)
        for rij in range(blok_rij * 3, blok_rij * 3 + 3)
        for kol in range(blok_kol * 3, blok_kol * 3 + 3)
    ]




    

if __name__ == "__main__":
    puzzles= read_puzzles("./Sudoku_puzzels_5.txt")
    first = puzzles[0]
    fixed = get_fixed_cells(first)
    print("Originele puzzel:")
    print_grid(first)

    print("\nStart-state (blokken gevuld met 1-9, fixed cells behouden):")
    start = generate_start_state(first, fixed)
    print_grid(start)
    #print(f"Aantal puzzels: {len(puzzles)}\n" )
    #print_grid(puzzles[0])
    # print("Originele puzzel:")
    # print_grid(first)

    # print("\nFixed-cellen matrix (True = vast, False = vrij):")
    # fixed = get_fixed_cells(first)
    # for row in fixed:
    #     print(row)



