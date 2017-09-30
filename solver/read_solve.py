from pprint import pprint
import numpy as np
import solver


def load_sudokus(N):
    quizzes = np.zeros((N, 81), np.int32)
    solutions = np.zeros((N, 81), np.int32)
    for i, line in enumerate(open('sudoku.csv', 'r').read().splitlines()[1:N+1]):
        quiz, solution = line.split(",")
        for j, q_s in enumerate(zip(quiz, solution)):
            q, s = q_s
            quizzes[i, j] = q
            solutions[i, j] = s
    quizzes = quizzes.reshape((-1, 9, 9))
    solutions = solutions.reshape((-1, 9, 9))
    return quizzes, solutions


if __name__ == '__main__':
    noq = 1
    quizzes, solutions = load_sudokus(noq)

    for i in np.arange(0, noq):
        quizz = quizzes[i].tolist()
        solution = solutions[i].tolist()

        pprint(quizz)

        solver.solve(quizz)

        if quizz == solution:
            print("Quizz {0} gives good solution".format(i+1))
        else:
            print("Quizz {0} sucks on solution".format(i+1))
            pprint(quizz)
            pprint(solution)
