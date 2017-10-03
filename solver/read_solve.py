from pprint import pprint
import numpy as np
import solver
from statistic import Statistic
from sudoku import Sudoku
import pandas as pd
import csv


def load_sudokus(dim, N):
    quizzes = np.zeros((N, dim ** 4), np.int32)
    solutions = np.zeros((N, dim ** 4), np.int32)
    for i, line in enumerate(open('../resources/sudoku_{}.csv'.format(dim), 'r').read().splitlines()[1:N + 1]):
        quiz, solution = line.split(",")
        for j, q_s in enumerate(zip(quiz.split(' '), solution.split(' '))):
            q, s = q_s[0], q_s[1]
            quizzes[i, j] = q
            solutions[i, j] = s
    quizzes = quizzes.reshape((-1, dim ** 2, dim ** 2))
    solutions = solutions.reshape((-1, dim ** 2, dim ** 2))
    return quizzes, solutions


def get_meaningful_statistics(captured_text):
    for line in captured_text.split('\n'):
        if len(line) >= 3 and line[2] == '1':
            status_list = line.split(" ")
            status_list = list(filter("".__ne__, status_list))
            status_list = status_list[2:]
            return Statistic(status_list[0], status_list[1], status_list[2], status_list[3],
                             status_list[4], status_list[5], status_list[6], status_list[7],
                             status_list[8], status_list[9])


if __name__ == '__main__':
    dim = 6
    noq = 10
    quizzes, solutions = load_sudokus(dim, noq)
    standard_clauses = solver.sudoku_clauses(dim)

    df = pd.DataFrame({'seconds':[], 'level':[], 'variables':[], 'used':[],
                        'original':[], 'conflicts':[], 'learned':[], 'limit':[],
                        'agility':[], 'MB':[]})
    df = df [['seconds', 'level', 'variables', 'used', 'original', 'conflicts',
              'learned', 'limit', 'agility', 'MB']]
    df.to_csv('stats_6.csv', index=False, sep=',')


    with open('stats_6.csv', 'a') as f:
        writer = csv.writer(f)
        for i in np.arange(0, noq):
            quiz = quizzes[i].tolist()
            solution = solutions[i].tolist()

            sudoku = Sudoku(quiz, solution, get_meaningful_statistics(solver.solve(quiz, standard_clauses)))

            if sudoku.puzzle == sudoku.solution:
                print(i)
                writer.writerow(sudoku.statistics.get_data())
                f.flush()
            else:
                print('not good')
