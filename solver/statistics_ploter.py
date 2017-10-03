import numpy as np
import matplotlib.pyplot as plt


def plot_statistics(sizes, means, stds):
    plt.figure(figsize=(16, 10), dpi=80)
    plt.xlabel('Sudoku size')
    plt.ylabel('Conflicts')
    plt.scatter(sizes, means, s=50, facecolors='none', edgecolors='blue', linewidth=1.5, zorder=2)
    plt.plot(sizes, means, color='#07c607', linewidth=1.5, zorder=3)
    # plt.fill_between(x_gen, means - stds, means + stds, alpha=0.2, color='#ffb6c1')
    # plt.xlim([0, 2 * np.pi])
    # plt.ylim([-1.5, 1.5])
    plt.show()


if __name__ == '__main__':
    plot_statistics([2, 3, 4, 5, 6],[1, 4, 8, 15, 20], [1, 2, 4, 6, 9])
