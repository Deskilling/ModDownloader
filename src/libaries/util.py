import os, requests, hashlib
from time import gmtime, strftime

log_filepath = "../../logs/" + strftime("%Y-%b-%d_%H-%M-%S", gmtime()) + ".log"

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

def change_exec_dir():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def sha1sum(filename,path):
    filename = path + filename
    with open(filename, "rb", buffering=0) as f:
        return hashlib.file_digest(f, "sha1").hexdigest()

def download_from_url(url, path, file_name):
    file_path = os.path.join(path, file_name)

    response = requests.get(url)
    if response.ok:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_path}")
