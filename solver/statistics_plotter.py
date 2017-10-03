import numpy as np
import matplotlib.pyplot as plt
from statistic import Statistic
from scipy.stats import norm


def plot_data():
    sizes = range(2, 7)
    means, stds = get_means_stds_for(sizes, file_name_templat="stats_{}")
    plot_statistics(sizes, means, stds)


def plot_statistics(sizes, mean_list, std_list):
    means = np.array(mean_list)
    stds = np.array(std_list)
    plt.figure(figsize=(16, 10), dpi=80)
    plt.xlabel('Sudoku size')
    plt.ylabel('Conflicts')
    plt.xticks(sizes)
    plt.scatter(sizes, means, s=50, facecolors='none', edgecolors='blue', linewidth=1.5, zorder=2)
    plt.plot(sizes, means, color='#07c607', linewidth=1.5, zorder=3)
    plt.fill_between(sizes, means - stds, means + stds, alpha=0.2, color='#ffb6c1')
    # plt.xlim([0, 2 * np.pi])
    # plt.ylim([-1.5, 1.5])
    plt.show()


def get_statistics(file_name):
    statistics = []
    for i, line in enumerate(open(file_name, 'r').read().splitlines()):
        tokens = line.split(",")
        statistics.append(
            Statistic(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4], tokens[5], tokens[6],
                      tokens[7], tokens[8], tokens[9]))
    return statistics


def get_means_stds_for(sizes, file_name_templat):
    means = []
    stds = []
    for size in sizes:
        conflicts = []
        for statistic in get_statistics(file_name_templat.format(size)):
            conflicts.append(statistic.conflicts)
        mean, std = get_mean_and_std(conflicts)
        means.append(mean)
        stds.append(std)

    return means, stds


def plot_conflict_distribution(data):
    # Fit a normal distribution to the data:
    mu, std = norm.fit(data)

    # Plot the histogram.
    plt.hist(data, bins=25, normed=True, alpha=0.6, color='g')

    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)

    plt.show()


def get_mean_and_std(data):
    norm.fit(data)


if __name__ == '__main__':
    plot_statistics([2, 3, 4, 5, 6], [1, 4, 8, 15, 20], [1, 2, 4, 6, 9])
