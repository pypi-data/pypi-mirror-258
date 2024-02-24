# -*- coding: utf-8 -*-
#######################################################################
# Testing memory utilization. This is used for the purpose of testing
#   of performance gains/loses for various approaches.
# Author: Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2021 Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
#######################################################################
import io
import tracemalloc
import gc
from itertools import groupby
from os.path import dirname, join, getsize
from parglare import Grammar, Parser, GLRParser
from tests import TESTS

INPUTS = 6
REPEAT = 5


class TestResult:
    def __init__(self, name):
        self.name = name
        self.input_idx = None
        self.size = None
        self.mem = None
        self.ambig = None


def mem_tests():
    results = []
    for test_idx, test in enumerate(TESTS):
        for parsing in ['LR', 'GLR']:
            if ((not test.lr and parsing == 'LR') or
                    (not test.glr and parsing == 'GLR')):
                continue

            parser_class = Parser if parsing == 'LR' else GLRParser
            for input_idx in range(INPUTS):
                result = TestResult(f'{test.name} {parsing}')
                result.input_idx = input_idx + 1
                test_root = join(dirname(__file__), f'test{test_idx+1}')
                file_name = join(test_root, f'input{input_idx+1}')
                result.size = getsize(file_name)

                g = Grammar.from_file(join(test_root, 'g.pg'))
                parser = parser_class(g)

                with io.open(file_name, 'r', encoding='utf-8') as f:
                    content = f.read()

                gc.collect()
                tracemalloc.start()
                forest = parser.parse(content)
                _, peak = tracemalloc.get_traced_memory()
                result.mem = peak // 1000
                tracemalloc.stop()

                if parsing == 'GLR':
                    result.ambig = forest.ambiguities

                results.append(result)

    with open(join(dirname(__file__), 'reports', 'mem-report.txt'), 'w') as f:
        inputs = '|'.join(f'    I{i+1}   ' for i in range(INPUTS))
        f.write(f'|               |{inputs}|\n')
        previous_name = 'None'
        for name, results in groupby(results, lambda r: r.name):
            results = list(results)
            if not name.startswith(previous_name):
                sizes_str = '|'.join(f'{r.size:^9,d}' for r in results)
                title = '{:15s}'.format(name[:-3] + ' sizes')
                f.write(f'|{title}|{sizes_str}|\n')
            results_str = '|'.join(f'{r.mem:^9,d}' for r in results)
            f.write(f'|{name:15s}|{results_str}|\n')
            if name.endswith('GLR'):
                ambig_str = '|'.join(f'{r.ambig:^9,d}' for r in results)
                title = '{:15s}'.format(name[:-4] + ' ambig')
                f.write(f'|{title}|{ambig_str}|\n')
            previous_name = ''.join(name.split()[:-1])


if __name__ == '__main__':
    mem_tests()
