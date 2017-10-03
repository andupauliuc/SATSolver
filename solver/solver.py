"""
The implementation of this Sudoku solver is based on the paper:
    "A SAT-based Sudoku solver" by Tjark Weber
    https://www.lri.fr/~conchon/mpri/weber.pdf
If you want to understand the code below, in particular the function valid(),
which calculates the 324 clauses corresponding to 9 cells, you are strongly
encouraged to read the paper first.  The paper is very short, but contains
all necessary information.
"""
import pycosat
import math

from c_stream_capturer import OutputGrabber


def v(i, j, d, size):
    """
    Return the number of the variable of cell i, j and digit d,
    which is an integer in the range of 1 to 729 (including).
    """
    return (size ** 4) * (i - 1) + (size ** 2) * (j - 1) + d


def sudoku_clauses(size):
    """
    Create the (????) Sudoku clauses, and return them as a list.
    Note that these clauses are *independent* of the particular
    Sudoku puzzle at hand.
    """
    res = []
    # for all cells, ensure that the each cell:
    for i in range(1, (size * size) + 1):
        for j in range(1, (size * size) + 1):
            # denotes (at least) one of the 9 digits (1 clause)
            res.append([v(i, j, d, size) for d in range(1, (size * size) + 1)])
            # does not denote two different digits at once (36 clauses)
            for d in range(1, (size * size) + 1):
                for dp in range(d + 1, (size * size) + 1):
                    res.append([-v(i, j, d, size), -v(i, j, dp, size)])

    def valid(cells):
        # Append ??? clauses, corresponding to 'size' cells, to the result.
        # The '' cells are represented by a list tuples.  The new clauses
        # ensure that the cells contain distinct values.
        for i, xi in enumerate(cells):
            for j, xj in enumerate(cells):
                if i < j:
                    for d in range(1, (size * size) + 1):
                        res.append([-v(xi[0], xi[1], d, size), -v(xj[0], xj[1], d, size)])

    # ensure rows and columns have distinct values
    for i in range(1, (size * size) + 1):
        valid([(i, j) for j in range(1, (size * size) + 1)])
        valid([(j, i) for j in range(1, (size * size) + 1)])
    # ensure 3x3 sub-grids "regions" have distinct values
    for i in range(1, (size * size), size):
        for j in range(1, (size * size), size):
            valid([(i + k % size, j + k // size) for k in range(size * size)])

    # assert len(res) == 81 * (1 + 36) + 27 * 324  # todo: change the hardcoded values
    return res


def solve(grid, standard_clauses):
    """
    solve a Sudoku grid inplace
    """
    size = math.floor(math.sqrt(len(grid)))  # todo: check if grid length is a squared number.
    # clauses = sudoku_clauses(size)
    clauses = list(standard_clauses)
    for i in range(1, (size * size) + 1):
        for j in range(1, (size * size) + 1):
            d = grid[i - 1][j - 1]
            # For each digit already known, a clause (with one literal).
            # Note:
            #     We could also remove all variables for the known cells
            #     altogether (which would be more efficient).  However, for
            #     the sake of simplicity, we decided not to do that.
            if d:
                clauses.append([v(i, j, d, size)])

    # wrap the method in an "OutputGrabber" to capture c-level statistics stream
    out = OutputGrabber()
    out.start()
    sol = set(pycosat.solve(clauses, verbose=1))  # solve the SAT problem
    out.stop()

    def read_cell(i, j, size):
        # return the digit of cell i, j according to the solution
        for d in range(1, (size * size) + 1):
            if v(i, j, d, size) in sol:
                return d

    for i in range(1, (size * size) + 1):
        for j in range(1, (size * size) + 1):
            grid[i - 1][j - 1] = read_cell(i, j, size)

    return out.capturedtext


if __name__ == '__main__':
    from pprint import pprint

    # hard Sudoku problem, see Fig. 3 in paper by Weber
    hard = [[0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 3],
            [0, 7, 4, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 0, 2],
            [0, 8, 0, 0, 4, 0, 0, 1, 0],
            [6, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 7, 8, 0],
            [5, 0, 0, 0, 0, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0]]
    solve(hard)
    pprint(hard)
    assert [[1, 2, 6, 4, 3, 7, 9, 5, 8],
            [8, 9, 5, 6, 2, 1, 4, 7, 3],
            [3, 7, 4, 9, 8, 5, 1, 2, 6],
            [4, 5, 7, 1, 9, 3, 8, 6, 2],
            [9, 8, 3, 2, 4, 6, 5, 1, 7],
            [6, 1, 2, 5, 7, 8, 3, 9, 4],
            [2, 6, 9, 3, 1, 4, 7, 8, 5],
            [5, 4, 8, 7, 6, 9, 2, 3, 1],
            [7, 3, 1, 8, 5, 2, 6, 4, 9]] == hard
