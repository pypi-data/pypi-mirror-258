import os
from shutil import rmtree


def create_empty_folder(path:str):
    if os.path.exists(path):
        rmtree(path)
    os.mkdir(path)