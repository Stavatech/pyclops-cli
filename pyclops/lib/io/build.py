import os
import shutil


BUILD_DIR = os.getenv('BUILD_DIR', './build')


def clean(path=BUILD_DIR):
    """ Clean the build directory """
    shutil.rmtree(path)