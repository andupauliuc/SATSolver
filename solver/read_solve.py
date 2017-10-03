from pprint import pprint
import numpy as np
import solver
from statistic import Statistic
from sudoku import Sudoku


def load_sudokus(dim, N):
    quizzes = np.zeros((N, dim ** 4), np.int32)
    solutions = np.zeros((N, dim ** 4), np.int32)
    for i, line in enumerate(open('../resources/sudoku_3.csv', 'r').read().splitlines()[1:N + 1]):
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
    dim = 3
    noq = 10
    quizzes, solutions = load_sudokus(dim, noq)

    for i in np.arange(0, noq):
        quiz = quizzes[i].tolist()
        solution = solutions[i].tolist()

        sudoku = Sudoku(quiz, solution, get_meaningful_statistics(solver.solve(quiz)))

        # print(sudoku.statistics)
        if sudoku.puzzle == sudoku.solution:
            print('all good')
        else:
            print('not good')

        # if quiz == solution:
        #     print("Quiz {0} gives good solution".format(i + 1))
        #     pprint(quiz)
        #
        # else:
        #     print("Quiz {0} sucks on solution".format(i + 1))
        #     pprint(quiz)
        #     pprint(solution)
