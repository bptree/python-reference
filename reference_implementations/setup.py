import sys

if sys.version_info < (3, 6):
  sys.stderr.write('Please run with Python 3.6\n')
  sys.exit(1)

from distutils.core import setup
from distutils.cmd import Command
import os
from os import path
import subprocess
from pathlib import Path

os.chdir(path.dirname(path.realpath(__file__)))


class OptionlessCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


TEST_ARGS = ['-m', 'unittest', 'discover', '.']


class TestCommand(OptionlessCommand):
    description = 'runs the unit and integration tests'

    def run(self):
        sys.exit(subprocess.call([sys.executable] + TEST_ARGS))


MODULES = ['countsketch', 'randomized']


class CoverageCommand(OptionlessCommand):
    description = 'measures code coverage of the unit and integration tests'

    def run(self):
        source = f"--source={','.join(MODULES)}"
        self._call_or_exit('Coverage', ['run', source] + TEST_ARGS)
        self._call_or_exit('Coverage report', ['report'])
        self._call_or_exit('Coverage html report', ['html', '-d', '.htmlcov',
                                                '--skip-covered'])

        uri = (Path(os.getcwd()) / '.htmlcov' / 'index.html').as_uri()
        print(f'\nView more detailed results at: {uri}')

    def _call_or_exit(self, name, args):
        exit_code = subprocess.call(['coverage-3.6'] + args)

        if exit_code != 0:
            print(f'{name} failed!', file=sys.stderr)
            sys.exit(exit_code)


class TypecheckCommand(OptionlessCommand):
    description = 'typechecks the code with mypy'

    def run(self):
        env = {'MYPYPATH': 'stubs', **os.environ}
        args = ['mypy', '--strict', '-i'] + MODULES
        sys.exit(subprocess.call(args, env=env))


class LintCommand(OptionlessCommand):
    description = 'lints the code with pycodestyle'

    def run(self):
        sys.exit(subprocess.call(['pycodestyle'] + MODULES))


setup(name='randomized',
      version='1.0',
      description='Randomized algorithm implementations',
      author='Bailey Parker',
      author_email='b@ileyparker.com',
      cmdclass={
        'test': TestCommand,
        'coverage': CoverageCommand,
        'typecheck': TypecheckCommand,
        'lint': LintCommand,
      })
