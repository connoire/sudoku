import csv
from possible import ROWS, COLS, BOXS, COMBOS, TARGET, calc_possible

# function to print puzzle
def print_puzzle(puzzle):

    for i in range(81):
        
        # number
        if puzzle[i] == 0:
            print(' -', end = '')
        else:
            print(f' {puzzle[i]}', end = '')
        
        # dividers
        if (i + 1) % 9 == 0:
            print('\n', end = '')
        elif (i + 1) % 3 == 0:
            print(' |', end = '')
        if (i + 1) % 27 == 0:
            if i != 80:
                print('-----------------------\n', end = '')
            else:
                print('\n', end = '')

# function to check if puzzle is solved
def is_solved(puzzle):
    
    # check if incomplete
    for i in puzzle:
        if i == 0:
            return False
    
    # check if all combos are complete
    for combo in COMBOS:
        if set(puzzle[i] for i in combo) != TARGET:
            return False
    
    return True

# function to solve a sudoku
def solve(puzzle, methods):

    print_puzzle(puzzle)
    iteration = 1
    prev = None
    possible = None

    # keep iterating until puzzle is solved
    while not is_solved(puzzle):

        print(f'Iteration {iteration}\n', end = '')

        # calc possible values for each cell
        possible = calc_possible(puzzle, methods, possible)

        # if cell only has one possible option, then update
        for i in range(81):
            if len(possible[i]) == 1:
                puzzle[i] = next(iter(possible[i]))
        
        # check if puzzle changed after this iteration
        if prev is not None and all(prev[i] == possible[i] for i in range(81)):
            print('Unsolvable from here')
            break
        else:
            print_puzzle(puzzle)

        prev = [set(s) for s in possible]        
        iteration += 1

# open puzzle and solve
with open('puzzle3.csv', 'r') as f:
    puzzle = list(csv.reader(f))[0]
    puzzle = list(map(int, puzzle))

solve(puzzle, methods = ['naked_singles', 'hidden_singles', 'naked_pairs', 'hidden_pairs'])