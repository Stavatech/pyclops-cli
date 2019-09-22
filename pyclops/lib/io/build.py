import os
import shutil


def clean(path):
    """ Clean the build directory """
    shutil.rmtree(path)