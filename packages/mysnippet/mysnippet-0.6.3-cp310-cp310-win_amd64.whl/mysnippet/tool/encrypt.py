# 对单文件加密

import click
import os
import shutil
import sys


def create_setup(filename):
    str = '''
from distutils.core import setup
from Cython.Build import cythonize


if __name__ == '__main__':
    setup(ext_modules = cythonize(r'{}', language_level=3))

    '''.format(filename)

    with open('setup.py', "w") as file:
        file.write(str)


@click.command()
@click.argument("filename", type=str)
def main(filename):
    _pwd = os.path.abspath(os.getcwd())

    filename = os.path.abspath(filename)
    _file_path = os.path.dirname(filename)
    try:
        os.chdir(_file_path)
        # create setup.py
        create_setup(os.path.basename(filename))

        # build
        python_executable = sys.executable
        os.system(f"{python_executable} setup.py build_ext --inplace")

        # clean
        shutil.rmtree("build")
        os.remove("setup.py")
        os.remove(filename.replace(".py", ".c"))
        # os.remove(filename)
    except Exception as e:
        raise Exception(e)
    finally:
        os.chdir(_pwd)
