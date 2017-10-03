import numpy as np
import matplotlib.pyplot as plt
from statistic import Statistic
from scipy.stats import norm

FILE_NAME_TEMPLATE = "stats_{}.csv"


def plot_memory():
    sizes = range(2, 6)
    funct = lambda x: x.MB
    means, stds = get_means_stds_for(sizes, FILE_NAME_TEMPLATE, funct)
    plot_statistics(sizes, means, stds, "Memory usage")


def plot_conflicts():
    sizes = range(2, 6)
    funct = lambda x: x.conflicts
    means, stds = get_means_stds_for(sizes, FILE_NAME_TEMPLATE, funct)
    plot_statistics(sizes, means, stds, "Conflicts")


def plot_learned_clauses():
    sizes = range(2, 6)
    funct = lambda x: x.learned
    means, stds = get_means_stds_for(sizes, FILE_NAME_TEMPLATE, funct)
    plot_statistics(sizes, means, stds, "Learned clauses")


def plot_run_time():
    sizes = range(2, 6)
    funct = lambda x: x.seconds
    means, stds = get_means_stds_for(sizes, FILE_NAME_TEMPLATE, funct)
    plot_statistics(sizes, means, stds, "Run time")


def plot_statistics(sizes, mean_list, std_list, y_label):
    means = np.array(mean_list)
    stds = np.array(std_list)
    fig = plt.figure(figsize=(16, 10), dpi=80)

    ax = fig.add_subplot(111)
    plt.xlabel('Sudoku size')
    plt.ylabel(y_label)
    plt.xticks(sizes)
    plt.scatter(sizes, means, s=50, facecolors='none', edgecolors='blue', linewidth=1.5, zorder=2)
    plt.plot(sizes, means, color='#07c607', linewidth=1.5, zorder=3)
    # plt.fill_between(sizes, means - stds, means + stds, alpha=0.2, color='#ffb6c1')
    for x, y in zip(sizes, means):  # <--
        ax.annotate(str(y), xy=(x, y + 500))
    # plt.xlim([0, 2 * np.pi])
    # plt.ylim([-1.5, 1.5])
    file_name = ''.join(x for x in y_label.title() if not x.isspace())
    # plt.savefig('../resources/plots/plot' + file_name + '.png') # THIS SAVES THE PLOT AS *.PNG
    plt.show()


def get_statistics(file_name):
    statistics = []
    for i, line in enumerate(open(file_name, 'r').read().splitlines()[1:]):
        tokens = line.split(",")
        statistics.append(
            Statistic(float(tokens[0]), float(tokens[1]), float(tokens[2]), float(tokens[3]),
                      float(tokens[4]), float(tokens[5]), float(tokens[6]),
                      float(tokens[7]), float(tokens[8]), float(tokens[9])))
    return statistics


def get_means_stds_for(sizes, file_name_template, funct):
    means = []
    stds = []
    for size in sizes:
        criteria = []
        for statistic in get_statistics(file_name_template.format(size)):
            criteria.append(funct(statistic))
        mean, std = get_mean_and_std(criteria)
        means.append(mean)
        stds.append(std)

    return means, stds


def plot_criteria_distribution(data,file_name):
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
    plt.savefig('../resources/plots/plot' + file_name + '.png') # THIS SAVES THE PLOT AS *.PNG
    plt.title(title)

    plt.show()


def get_mean_and_std(data):
    mean, std = norm.fit(data)
    return round(mean, 2), round(std, 2)


def plot_conflict_distribution_for(size):
    conflicts = []
    for statistic in get_statistics(FILE_NAME_TEMPLATE.format(size)):
        conflicts.append(statistic.conflicts)
    plot_criteria_distribution(conflicts, "Conflicts" + str(size))


if __name__ == '__main__':
    pass
    # plot_memory()
    # plot_learned_clauses()
    # plot_run_time()
    # plot_conflicts()
    plot_conflict_distribution_for(5)
