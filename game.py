PUZZLE = [3, 0, 0, 9, 6, 7, 0, 0, 1, 
          0, 4, 0, 3, 0, 2, 0, 8, 0, 
          0, 2, 0, 0, 0, 0, 0, 7, 0, 
          0, 7, 0, 0, 0, 0, 0, 9, 0, 
          0, 0, 0, 8, 7, 3, 0, 0, 0, 
          5, 0, 0, 0, 1, 0, 0, 0, 3, 
          0, 0, 4, 7, 0, 5, 1, 0, 0, 
          9, 0, 5, 0, 0, 0, 2, 0, 7, 
          8, 0, 0, 6, 2, 1, 0, 0, 4]

ROWS = [[ 0,  1,  2,  3,  4,  5,  6,  7,  8], 
        [ 9, 10, 11, 12, 13, 14, 15, 16, 17], 
        [18, 19, 20, 21, 22, 23, 24, 25, 26], 
        [27, 28, 29, 30, 31, 32, 33, 34, 35], 
        [36, 37, 38, 39, 40, 41, 42, 43, 44], 
        [45, 46, 47, 48, 49, 50, 51, 52, 53], 
        [54, 55, 56, 57, 58, 59, 60, 61, 62], 
        [63, 64, 65, 66, 67, 68, 69, 70, 71], 
        [72, 73, 74, 75, 76, 77, 78, 79, 80]]

COLS = [[ 0,  9, 18, 27, 36, 45, 54, 63, 72], 
        [ 1, 10, 19, 28, 37, 46, 55, 64, 73], 
        [ 2, 11, 20, 29, 38, 47, 56, 65, 74], 
        [ 3, 12, 21, 30, 39, 48, 57, 66, 75], 
        [ 4, 13, 22, 31, 40, 49, 58, 67, 76], 
        [ 5, 14, 23, 32, 41, 50, 59, 68, 77], 
        [ 6, 15, 24, 33, 42, 51, 60, 69, 78], 
        [ 7, 16, 25, 34, 43, 52, 61, 70, 79], 
        [ 8, 17, 26, 35, 44, 53, 62, 71, 80]]

SQRS = [[ 0,  1,  2,  9, 10, 11, 18, 19, 20], 
        [ 3,  4,  5, 12, 13, 14, 21, 22, 23], 
        [ 6,  7,  8, 15, 16, 17, 24, 25, 26], 
        [27, 28, 29, 36, 37, 38, 45, 46, 47], 
        [30, 31, 32, 39, 40, 41, 48, 49, 50], 
        [33, 34, 35, 42, 43, 44, 51, 52, 53], 
        [54, 55, 56, 63, 64, 65, 72, 73, 74], 
        [57, 58, 59, 66, 67, 68, 75, 76, 77], 
        [60, 61, 62, 69, 70, 71, 78, 79, 80]]

COMBOS = ROWS + COLS + SQRS

TARGET = {1, 2, 3, 4, 5, 6, 7, 8, 9}

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

# simple function to find what numbers are possible in each cell (from what exists in its row, col, sqr)
def calc_possible(puzzle):

    possible = [None] * 81

    for i in range(81):
        
        # check if already solved
        if puzzle[i] != 0:
            possible[i] = [puzzle[i]]
            continue
        
        # calculate row, col, sqr the cell belongs to
        r = i // 9
        c = i % 9
        s = (r // 3) * 3 + (c // 3)

        # find all numbers that already exist in row, col, sqr
        used = set()
        used.update(puzzle[j] for j in ROWS[r])
        used.update(puzzle[j] for j in COLS[c])
        used.update(puzzle[j] for j in SQRS[s])
        used.discard(0)

        possible[i] = [k for k in TARGET if k not in used]
    
    return possible

# function to solve a sudoku
def solve(puzzle):

    print_puzzle(puzzle)
    iter = 0

    # keep iterating until puzzle is solved
    while not is_solved(puzzle):

        print(f'Iteration {iter}\n', end = '')

        # calc possible values for each cell
        possible = calc_possible(puzzle)

        # if cell only has one possible option, then update
        changed = False
        for i in range(81):
            if len(possible[i]) == 1:
                puzzle[i] = possible[i][0]
                changed = True
        
        # check if the puzzle changed after this iteration
        if changed == False:
            print('Unsolvable from here')
            break
        else:
            print_puzzle(puzzle)

        iter += 1

solve(PUZZLE.copy())