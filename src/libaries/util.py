import os
from time import gmtime, strftime

log_filepath = "../../logs/" + strftime("%d_%b_%Y_%H_%M_%S",gmtime()) + ".log" 

def change_exec_dir():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

def create_logfile():
    if not os.path.exists("../../logs"):
        os.mkdir("../../logs")
    open(log_filepath,"x")
    file = open(log_filepath,"a")
    file.write(f"Exec Time: {strftime("%d_%b_%Y_%H_%M_%S",gmtime())}")

def log(was):
    time = f"[{strftime("%d_%b_%Y_%H-%M-%S", gmtime())}]"
    file = open(log_filepath,"a")
    file.write(f"\n{time}: {was}")