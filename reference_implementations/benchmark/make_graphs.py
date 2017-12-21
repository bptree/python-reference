from argparse import ArgumentParser
from benchmark.parse_cprofile import parse as parse_cprofile
from collections import OrderedDict
from csv import writer as CsvWriter
from glob import iglob as glob
from itertools import count, product
from pathlib import Path
import sys


COLUMNS = ('ncalls', 'tottime', 'tot_percall', 'cumtime', 'cum_percall')


def main():
    args = get_args()
    data = extract_columns(args, get_data(args))

    csv_writer = CsvWriter(sys.stdout)

    # Algorithms headers
    csv_writer.writerow(['row'] + flatten([algorithm] * count_columns(d)
                                          for algorithm, d in data.items()))
    # Stream Size Headers
    csv_writer.writerow(['row'] + flatten([size] * count_columns(d)
                                          for _, d in data.items()
                                          for size, d in d.items()))
    # Column Headers
    csv_writer \
        .writerow(['row \ col'] + [col for _, d in data.items()
                                       for _, d in d.items()
                                       for col, d in first_value(d).items()])

    algorithms, sizes, rows, cols = get_keys(data)
    for row in rows:
        csv_writer.writerow([row] + [value for _, d in data.items()
                                           for _, d in d.items()
                                           for value in d[row].values()])


def count_columns(data):
    first_dimension = first_value(data)
    second_dimension = first_value(first_dimension)

    if not isinstance(second_dimension, dict):
        return len(first_dimension)
    else:
        return len(data) * count_columns(first_dimension)


def flatten(lst):
    return sum(lst, [])


def get_keys(data):
    first_dimension = first_value(data)
    second_dimension = first_value(first_dimension)
    third_dimension = first_value(second_dimension)

    algorithms = tuple(data.keys())
    sizes = tuple(first_dimension.keys())
    rows = tuple(second_dimension.keys())
    cols = tuple(third_dimension.keys())

    return algorithms, sizes, rows, cols


def first_value(d):
    return list(d.values())[0]


def extract_columns(args, data):
    all_algorithms = tuple(data.keys())
    all_sizes = tuple(data[all_algorithms[0]].keys())

    algorithms = tuple([args.algorithm]) if args.algorithm else all_algorithms
    sizes = tuple(map(int, args.sizes.split())) if args.sizes else all_sizes

    extracted_data = OrderedDict()

    for algorithm, size in product(algorithms, sizes):
        extracted_data.setdefault(algorithm, OrderedDict())[size] = \
            OrderedDict((j, OrderedDict((i, merge_column(args, iters))
                                        for i, iters in row.items()))
                        for j, row in data[algorithm][size].items())

    return extracted_data


def merge_column(args, iters):
    return mean([extract_column(args, i) for i in iters])


def median(numbers):
    numbers = sorted(numbers)
    return numbers[len(numbers) // 2]


def mean(numbers):
    return sum(numbers) / len(numbers)


def extract_column(args, iteration):
    try:
        stat = list(filter(lambda s: args.function_name in s.name,
                           iteration.functions))[0]
        return getattr(stat, args.column)
    except IndexError:
        run_name = "alg={} size={} cols={}" \
            .format(iteration.algorithm, iteration.size, iteration.rows,
                    iteration.cols)
        raise Exception("Run {} missing function '{}'" \
            .format(run_name, args.function_name))


def get_data(args):
    data = OrderedDict()

    for r in sorted(get_run_results(args)):
        data \
            .setdefault(r.algorithm, OrderedDict()) \
            .setdefault(r.size, OrderedDict()) \
            .setdefault(r.rows, OrderedDict()) \
            .setdefault(r.cols, []) \
            .append(r)

    assert is_dense(data), 'data is not dense'
    return data


def get_run_results(args):
    for path in glob(str(args.result_dir / '**' / '*.txt'), recursive=True):
        yield parse_cprofile(path)


def is_dense(data):
    # For a valid CSV to be produced we must have a dense data matrix.
    # Because the matrix is constructed from dicts, it is possible that
    # for example len(data['bptree']) != len(data['countsketch']), which
    # would make it impossible to output a dense rectangular CSV.
    for i in count(1):
        level = list(get_dicts_at_level(data, i))

        if len(level) == 0:
            return True

        if len(set(map(len, level))) != 1:
            print(i)
            print([d.keys() for d in get_dicts_at_level(data, i - 1)])
            print(list(map(len, level)))
            return False


def get_dicts_at_level(parent, level):
    assert level >= 0, 'level must be non-negative'

    if level == 0:
        if isinstance(parent, dict):
            yield parent
    else:
        for d in parent.values():
            yield from get_dicts_at_level(d, level - 1)


def get_args():
    parser = ArgumentParser(description='parse cprofile output into CSVs')
    parser.add_argument('result_dir', type=Path)
    parser.add_argument('function_name')
    parser.add_argument('column', choices=COLUMNS)
    parser.add_argument('--algorithm')
    parser.add_argument('--sizes')

    return parser.parse_args()


if __name__ == '__main__':
    main()
