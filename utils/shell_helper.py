
from subprocess import check_output


def run_sh_file(file_path):
    stdout = check_output([file_path]).decode('utf-8')
    return stdout