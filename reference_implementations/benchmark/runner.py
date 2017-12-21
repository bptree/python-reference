from argparse import ArgumentParser
from benchmark.distributions import zipf
from bptree import BpTree
from contextlib import redirect_stdout
from collections import Counter
import cProfile
from countsketch import Counter as CountSketch
from io import StringIO
from itertools import product
from multiprocessing import Pool
from pathlib import Path
from random import randint


class Runner:
    def __init__(self, algorithm, distribution):
        self.algorithm = algorithm
        self.distribution = distribution

    def run(self):
        self.algorithm.add_items(self.distribution)
        self.most_common = self.algorithm.most_common()


def countsketch(rows, cols):
    return CountSketch(rows, cols, K)


def bptree(rows, cols):
    return BpTree(rows, cols, 5)


K = 3
ALGORITHMS = {'countsketch': countsketch, 'bptree': bptree}
DISTRIBUTIONS = {'zipf': zipf}
SIZES = (100000, 500000, 1000000)
ROWS = (1, 10, 50, 100)
COLS = (4, 16, 32, 64)


def main():
    args = get_args()
    args.dest_dir.mkdir(parents=True, exist_ok=True)

    runs = product((args.dest_dir,),
                   product(ALGORITHMS.keys(), DISTRIBUTIONS.keys(), SIZES,
                           ROWS, COLS, range(args.iterations)))

    with Pool() as pool:
        for done in pool.imap_unordered(pool_run, runs):
            print(done)


def pool_run(args):
    dest_dir, args = args
    algorithm, distribution, *rest = args
    return run(dest_dir, ALGORITHMS[algorithm], DISTRIBUTIONS[distribution],
               *rest)


def run(dest_dir, algorithm, distribution, size, rows, cols, iteration):
    name_parts = (algorithm.__name__, distribution.__name__, size, rows, cols,
                  iteration)
    path = dest_dir / "{}.txt".format('_'.join(map(str, name_parts)))

    seed = randint(0, 2**31)
    runner = Runner(algorithm(rows, cols), distribution(seed, size))

    with open(str(path), 'w') as f:
        profile_output = StringIO()
        with redirect_stdout(profile_output):
            cProfile.runctx('runner.run()', globals(), locals())
        print(profile_output.getvalue(), file=f)

        ground_truth = Counter(distribution(seed, size)).most_common(K)
        reported = runner.most_common

        correct = compute_correct(ground_truth, reported)
        errors = list(compute_error(ground_truth, reported))

        print('\ncorrect: {} ({}%)'.format(correct, sum(correct) / K * 100),
              file=f)
        print('errors {} (avg={}, sum={})' \
                .format(errors, sum(errors) / K, sum(errors)), file=f)

    return "alg={} dist={} len={} rows={} cols={} iter={}".format(*name_parts)


def compute_correct(ground_truth, reported):
    reported_hhs = [hh for hh, _ in reported]
    return [true_hh in reported_hhs for true_hh, _ in ground_truth]


def compute_error(ground_truth, reported):
    for true_hh, true_freq in ground_truth:
        for reported_hh, reported_freq in reported:
            if reported_hh == true_hh:
                yield abs(true_freq - reported_freq) / true_freq * 100
                break
        else:
            yield float('inf')


def get_args():
    parser = ArgumentParser(description='run countsketch/bptree benchmarks')
    parser.add_argument('dest_dir', type=Path)
    parser.add_argument('--iterations', type=int, default=5)

    return parser.parse_args()


if __name__ == '__main__':
    main()
