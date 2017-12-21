from collections import namedtuple
from os.path import basename


RunResult = namedtuple('RunResult', ('algorithm', 'distribution', 'size',
                                     'rows', 'cols', 'iteration', 'functions',
                                     'correct', 'errors'))
FunctionStat = namedtuple('FunctionStat', ('ncalls', 'tottime', 'tot_percall',
                                           'cumtime', 'cum_percall', 'name'))


def parse(path):
    filename_parts = basename(path).split('.')[0].split('_')
    algorithm, distribution = filename_parts[:2]
    size, rows, cols, iteration = map(int, filename_parts[2:])

    with open(path, 'r') as f:
        lines = iter(f)
        _read_until_functions(lines)
        functions = list(_read_functions(lines))
        correct, errors = _read_postamble(lines)

    return RunResult(algorithm, distribution, size, rows, cols, iteration,
                     functions, correct, errors)


def _read_until_functions(lines):
    for line in lines:
        if 'ncalls' in line:
            break


def _read_functions(lines):
    for line in lines:
        if line.strip() == '':
            return

        columns = line.split()

        ncalls = int(columns[0].split('/')[0])
        tottime, tot_percall, cumtime, cum_percall = map(float, columns[1:5])
        name = ' '.join(columns[5:])

        yield FunctionStat(ncalls, tottime, tot_percall, cumtime, cum_percall,
                           name)


def _read_postamble(lines):
    for line in lines:
        if 'correct: ' in line:
            left_bracket, right_bracket = line.find('['), line.rfind(']')
            between_brackets = line[left_bracket+1:right_bracket]
            correct = list(map(bool, between_brackets.split(', ')))
            break

    for line in lines:
        if 'errors ' in line:
            left_bracket, right_bracket = line.find('['), line.rfind(']')
            between_brackets = line[left_bracket+1:right_bracket]
            errors = list(map(float, between_brackets.split(', ')))
            break

    return correct, errors
