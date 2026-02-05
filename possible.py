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

# calculate what numbers are possible in each cell, with user input method choices
def calc_possible(puzzle, methods = None):

    if methods == None:
        methods = ['naked_singles']
    possible = naked_singles(puzzle)

    if 'hidden_singles' in methods:
        possible = hidden_singles(puzzle, possible)

    return possible

# naked singles: take every cell and check for all numbers in its row, col, sqr, the cell number cannot be any of these
def naked_singles(puzzle):

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

# hidden singles: take every combo and find what numbers are missing, if a number is missing and possible only in one cell it must be that
def hidden_singles(puzzle, possible):

    for combo in COMBOS:

        for j in TARGET:
            
            # find cells each target number can be in
            spots = [i for i in combo if puzzle[i] == 0 and j in possible[i]]

            # find if target number can only be in one cell
            if len(spots) == 1:
                possible[spots[0]] = [j]
                
    return possible