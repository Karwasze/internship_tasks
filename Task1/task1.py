import sys
import csv


indices = []
story_points = []
ksp = []
results = []


def sanitize_input():
    """Checks whether the arguments are correct"""
    if sys.argv[2].isdigit() is False:
        raise Exception("Second argument must be a digit!")
    if int(sys.argv[2]) <= 0:
        raise Exception("Second argument must be larger than 0!")
    if sys.argv[1][-3:] != "csv":
        raise Exception("Wrong file format!")
    file = open(sys.argv[1], 'r')
    contents = csv.reader(file, delimiter=",")
    row = next(contents)
    if row != ['task_id', 'story_points', 'KSP']:
        raise Exception("Wrong layout of csv file!")
    else:
        file.close()
        return


def file_handler():
    """
    Handler for file opening, uses csv reader
    to easily access rows from a given file.
    Handler skips first row containing headers,
    and appends values to global lists
    containing indices, story points, and ksp
    """
    file = open(sys.argv[1], 'r')
    contents = csv.reader(file, delimiter=",")
    next(contents)
    for row in contents:
        indices.append(int(row[0]))
        story_points.append(int(row[1]))
        ksp.append(int(row[2]))
    file.close()


def knapsack():
    """
    Function that implements
    1/0 knapsack problem with
    additional array backtracking
    to find desired items
    """
    velocity = int(sys.argv[2])
    n = len(indices)

    solver = [[0 for v in range(velocity+1)] for i in range(n+1)]
    for i in range(n+1):
        for v in range(velocity+1):
            if i == 0 or v == 0:
                solver[i][v] = 0
            elif story_points[i - 1] <= v:
                solver[i][v] = max(ksp[i - 1] +
                                    solver[i - 1][v - story_points[i - 1]],
                                    solver[i - 1][v])
            else:
                solver[i][v] = solver[i - 1][v]
    max_val = solver[n][velocity]
    v = velocity
    for i in range(n, 0, -1):
        if max_val <= 0:
            break
        if max_val == solver[i - 1][v]:
            continue
        else:
            results.append(indices[i - 1])
            max_val = max_val - ksp[i - 1]
            v = v - story_points[i - 1]



def show_results():
    """Pretty printing results"""
    results.sort()
    print(','.join(map(str, results)))



if __name__ == '__main__':
    sanitize_input()
    file_handler()
    knapsack()
    show_results()
