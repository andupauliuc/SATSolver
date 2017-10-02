from pprint import pprint
import numpy as np
import solver
from statistic import Statistic


def load_sudokus(N):
    quizzes = np.zeros((N, 81), np.int32)
    solutions = np.zeros((N, 81), np.int32)
    for i, line in enumerate(open('..\\resources\\sudoku.csv', 'r').read().splitlines()[1:N + 1]):
        quiz, solution = line.split(",")
        for j, q_s in enumerate(zip(quiz, solution)):
            q, s = q_s
            quizzes[i, j] = q
            solutions[i, j] = s
    quizzes = quizzes.reshape((-1, 9, 9))
    solutions = solutions.reshape((-1, 9, 9))
    return quizzes, solutions


def get_meaningful_statistics(capturedtext):
    for line in capturedtext.split('\n'):
        if len(line) >= 3 and line[2] == '1':
            status_list = line.split(" ")
            status_list = list(filter("".__ne__, status_list))
            status_list = status_list[2:]
            return Statistic(status_list[0], status_list[1], status_list[2], status_list[3],
                             status_list[4], status_list[5], status_list[6], status_list[7],
                             status_list[8], status_list[9])


if __name__ == '__main__':
    noq = 70
    quizzes, solutions = load_sudokus(noq)

    for i in np.arange(0, noq):
        quiz = quizzes[i].tolist()
        solution = solutions[i].tolist()

        print(str(get_meaningful_statistics(solver.solve(quiz))))

        # if quiz == solution:
        #     print("Quiz {0} gives good solution".format(i + 1))
        #     pprint(quiz)
        #
        # else:
        #     print("Quiz {0} sucks on solution".format(i + 1))
        #     pprint(quiz)
        #     pprint(solution)
