import numpy as np
import solver
from sudoku import Sudoku
import pandas as pd


def load_sudokus(dim, N):
    quizzes = np.zeros((N, dim ** 4), np.int32)
    solutions = np.zeros((N, dim ** 4), np.int32)
    for i, line in enumerate(open('../resources/test.csv'.format(dim), 'r').read().splitlines()[1:N + 1]):
        quiz, solution = line.split(",")
        for j, q_s in enumerate(zip(quiz.split(' '), solution.split(' '))):
            q, s = q_s[0], q_s[1]
            quizzes[i, j] = q
            solutions[i, j] = s
    quizzes = quizzes.reshape((-1, dim ** 2, dim ** 2))
    solutions = solutions.reshape((-1, dim ** 2, dim ** 2))
    return quizzes, solutions


if __name__ == '__main__':
    dim = 4
    noq = 1
    quizzes, solutions = load_sudokus(dim, noq)
    standard_clauses = solver.sudoku_clauses(dim)

    print(len(standard_clauses))
