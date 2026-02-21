from collections import defaultdict as dd
import itertools

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

BOXS = [[ 0,  1,  2,  9, 10, 11, 18, 19, 20], 
        [ 3,  4,  5, 12, 13, 14, 21, 22, 23], 
        [ 6,  7,  8, 15, 16, 17, 24, 25, 26], 
        [27, 28, 29, 36, 37, 38, 45, 46, 47], 
        [30, 31, 32, 39, 40, 41, 48, 49, 50], 
        [33, 34, 35, 42, 43, 44, 51, 52, 53], 
        [54, 55, 56, 63, 64, 65, 72, 73, 74], 
        [57, 58, 59, 66, 67, 68, 75, 76, 77], 
        [60, 61, 62, 69, 70, 71, 78, 79, 80]]

COMBOS = ROWS + COLS + BOXS

TARGET = {1, 2, 3, 4, 5, 6, 7, 8, 9}

# calculate what numbers are possible in each cell, with user input method choices
def calc_possible(puzzle, methods, possible):

    if 'naked_singles' in methods:
        possible = naked_singles(puzzle, possible)

    if 'hidden_singles' in methods:
        possible = hidden_singles(puzzle, possible)
    
    if 'naked_pairs' in methods:
        possible = naked_pairs(puzzle, possible)

    if 'hidden_pairs' in methods:
        possible = hidden_pairs(puzzle, possible)

    if 'naked_triples' in methods:
        possible = naked_triples(puzzle, possible)

    if 'hidden_triples' in methods:
        possible = hidden_triples(puzzle, possible)

    return possible

# naked singles: take every cell and check for all numbers in its row, col, box, the cell number cannot be any of these
def naked_singles(puzzle, possible):

    if possible == None:
        possible = [None] * 81

    for i in range(81):
        
        # check if already solved
        if puzzle[i] != 0:
            possible[i] = {puzzle[i]}
            continue
        
        # calculate row, col, box the cell belongs to
        r = i // 9
        c = i % 9
        b = (r // 3) * 3 + (c // 3)

        # find all numbers that already exist in row, col, box
        used = set()
        used.update(puzzle[j] for j in ROWS[r])
        used.update(puzzle[j] for j in COLS[c])
        used.update(puzzle[j] for j in BOXS[b])
        used.discard(0)

        # on first iteration remove from all possible numbers
        if possible[i] is None:
            possible[i] = TARGET - used

        # otherwise remove from already existing list
        else:
            possible[i] = possible[i] - used
    
    return possible

# hidden singles: take every combo and find what numbers are missing, if a number is missing and possible only in one cell it must be that
def hidden_singles(puzzle, possible):

    for combo in COMBOS:

        for i in TARGET:
            
            # find cells each target number can be in
            spots = [j for j in combo if puzzle[j] == 0 and i in possible[j]]

            # find if target number can only be in one cell
            if len(spots) == 1:
                possible[spots[0]] = {i}
                
    return possible

# naked pairs: take every combo and find candidate pairs, then remove those 2 values from other cells in same row, col, box
def naked_pairs(puzzle, possible):

    for combo in COMBOS:

        # find cells with 2 possible numbers
        pair_map = dd(list)
        for i in combo:
            if len(possible[i]) == 2:
                pair_map[tuple(sorted(possible[i]))].append(i)

        # find a pair of these numbers
        for pair, cells in pair_map.items():
            if len(cells) == 2:

                # remove pair from all other cells in the combo
                for i in combo:
                    if i in cells or puzzle[i] != 0:
                        continue
                    else:
                        possible[i] = possible[i] - set(pair)

    return possible

# hidden pairs: take every combo and find a pair that can only be in the same 2 cells, then remove all other values from those cells
def hidden_pairs(puzzle, possible):

    for combo in COMBOS:

        # find what cells each number can be in
        value_map = {i: [j for j in combo if puzzle[j] == 0 and i in possible[j]] for i in TARGET}

        # check every pair of numbers
        for i in range(1, 10):
            for j in range(i + 1, 10):
                cells_1 = value_map[i]
                cells_2 = value_map[j]

                # check if it is a hidden pair
                if cells_1 == cells_2 and len(cells_1) == 2:
                    pair_cells = cells_1
                    pair = {i, j}

                    # remove all other numbers from the pair cells
                    for cell in pair_cells:
                        if possible[cell] != pair:
                            possible[cell] = pair

    return possible

# naked triples: take every combo and find candidate triples, then remove those 3 values from other cells in same row, col, box
def naked_triples(puzzle, possible):

    for combo in COMBOS:

        # find cells that have at most three numbers
        candidate_cells = [i for i in combo if puzzle[i] == 0 and 1 <= len(possible[i]) <= 3]

        # find a triple of these numbers
        for cells in itertools.combinations(candidate_cells, 3):
            triple_vals = set().union(*(possible[i] for i in cells))
            if len(triple_vals) == 3:

                # remove triple from all other cells in the combo
                for i in combo: 
                    if i in cells or puzzle[i] != 0:
                        continue

                    new_possible = possible[i] - triple_vals
                    if possible[i] != new_possible:
                        possible[i] = new_possible

    return possible

# hidden triples: take every combo and find a triple that can only be in the same 3 cells, then remove all other values from those cells
def hidden_triples(puzzle, possible):

    for combo in COMBOS:

        # find what cells each number can be in
        value_map = {i: [j for j in combo if puzzle[j] == 0 and i in possible[j]] for i in TARGET}

        # check every triple of numbers
        for i, j, k in itertools.combinations(TARGET, 3):
            triple_cells = set(value_map[i]) | set(value_map[j]) | set(value_map[k])

            # check if it is a hidden triple
            if len(triple_cells) == 3 and all(len(value_map[x]) > 0 for x in (i, j, k)):
                
                # remove all other numbers from the triple cells
                for cell in triple_cells:
                    new_possible = possible[cell] & {i, j, k}
                    if possible[cell] != new_possible:
                        possible[cell] = new_possible

    return possible

# naked quads: take every combo and find candidate quads, then remove those 4 values from other cells in same row, col, box
def naked_quads(puzzle, possible):

    for combo in COMBOS:

        # find cells that have at most four numbers
        candidate_cells = [i for i in combo if puzzle[i] == 0 and 1 <= len(possible[i]) <= 4]

        # find a quad of these numbers
        for cells in itertools.combinations(candidate_cells, 4):
            quad_vals = set().union(*(possible[i] for i in cells))
            if len(quad_vals) == 4:

                # remove quad from all other cells in the combo
                for i in combo: 
                    if i in cells or puzzle[i] != 0:
                        continue

                    new_possible = possible[i] - quad_vals
                    if possible[i] != new_possible:
                        possible[i] = new_possible

    return possible

# hidden quads: take every combo and find a quad that can only be in the same 4 cells, then remove all other values from those cells
def hidden_quads(puzzle, possible):

    for combo in COMBOS:

        # find what cells each number can be in
        value_map = {i: [j for j in combo if puzzle[j] == 0 and i in possible[j]] for i in TARGET}

        # check every quad of numbers
        for i, j, k, l in itertools.combinations(TARGET, 4):
            quad_cells = set(value_map[i]) | set(value_map[j]) | set(value_map[k]) | set(value_map[l])

            # check if it is a hidden quad
            if len(quad_cells) == 4 and all(len(value_map[x]) > 0 for x in (i, j, k, l)):
                
                # remove all other numbers from the quad cells
                for cell in quad_cells:
                    new_possible = possible[cell] & {i, j, k, l}
                    if possible[cell] != new_possible:
                        possible[cell] = new_possible

    return possible