import os

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, path):
        self.newPath = path

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)