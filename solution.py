import itertools

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy only on the columns.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    # Diagonals are excluded as they are not used in naked_twins
    for unit in row_units + column_units + square_units:
        d = dict()
        for digit in cols:
            # get all boxes in the unit that have the digit
            boxes_with_digit = ''.join([box for box in unit if digit in values[box]])
            if len(boxes_with_digit) == 4:
                # Assign only pair of boxes(4chars) to keys in dict 
                if (boxes_with_digit not in d.keys()): 
                    # print('inserting:', digit, ' in ', boxes_with_digit)
                    d[boxes_with_digit] = digit
                # 2 similar digits are found if repeated pair of boxes are found
                else:
                    digits = d[boxes_with_digit] + digit
                    for box in unit:
                        if (box in boxes_with_digit):
                            # These 2 boxes must have only these 2 values
                            assign_value(values, box, digits) #values[box] = digits
                        else:
                            # The rest of the boxes cannot have these digits
                            assign_value(values, box, values[box].replace(digits[0], ""))
                            assign_value(values, box, values[box].replace(digits[1], ""))
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grid_l = list(grid)
    for i in range(len(grid_l)):
        if grid_l[i] == '.':
            grid_l[i] = '123456789'
    return dict(zip(boxes, grid_l))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    solved_values_not = [box for box in values.keys() if len(values[box]) != 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
                #values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Use naked_twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[box])==1 for box in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    n,mbox = min((len(values[box]),box) for box in boxes if len(values[box])>1)
    #print("find min box",mbox, n)
    #display(values)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[mbox]:
        branch_sudoku = values.copy()
        branch_sudoku[mbox] = value
        #print("searching...")
        attempt = search(branch_sudoku)
        if attempt:
            #print("inside", mbox, value)
            #display(attempt)
            return attempt
        else:
            #print("attempt failed", mbox, value, attempt)
            display(branch_sudoku)

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return(search(grid_values(grid)))

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal1 = [[r+c for (r,c) in zip(rows, cols)]]
diagonal2 = [[r+c for (r,c) in zip(rows, reversed(cols))]]
unitlist = row_units + column_units + square_units + diagonal1 + diagonal2
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    unsolved = {"G7": "1569", "G6": "134568", "G5": "13568", "G4": "134568", "G3": "2", "G2": "34589", "G1": "7", "G9": "5689", "G8": "15", "C9": "56", "C8": "3", "C3": "7", "C2": "1245689", "C1": "1245689", "C7": "2456", "C6": "1245689", "C5": "12568", "C4": "1245689", "E5": "4", "E4": "135689", "F1": "1234589", "F2": "12345789", "F3": "34589", "F4": "123589", "F5": "12358", "F6": "123589", "F7": "14579", "F8": "6", "F9": "3579", "B4": "1234567", "B5": "123567", "B6": "123456", "B7": "8", "B1": "123456", "B2": "123456", "B3": "345", "B8": "9", "B9": "567", "I9": "578", "I8": "27", "I1": "458", "I3": "6", "I2": "458", "I5": "9", "I4": "124578", "I7": "3", "I6": "12458", "A1": "2345689", "A3": "34589", "A2": "2345689", "E9": "2", "A4": "23456789", "A7": "24567", "A6": "2345689", "A9": "1", "A8": "4", "E7": "159", "E6": "7", "E1": "135689", "E3": "3589", "E2": "135689", "E8": "15", "A5": "235678", "H8": "27", "H9": "4", "H2": "3589", "H3": "1", "H1": "3589", "H6": "23568", "H7": "25679", "H4": "235678", "H5": "235678", "D8": "8", "D9": "3579", "D6": "123569", "D7": "14579", "D4": "123569", "D5": "12356", "D2": "12345679", "D3": "3459", "D1": "1234569"} 
    print("unsolved")
    display(unsolved)
    print("-----------------")
    display(solve(diag_sudoku_grid))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
