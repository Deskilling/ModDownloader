import os
def change_exec_dir():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)