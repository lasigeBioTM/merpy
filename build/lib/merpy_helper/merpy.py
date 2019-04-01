import os
from subprocess import Popen, PIPE

_mer_path = "data/MER/"


def generate_lexicon(filename):
    pass


def get_entities(text, lexicon):
    cwd = os.getcwd()
    os.chdir(_mer_path) 
    session = Popen(['./get_entities.sh', text, lexicon], stdout=PIPE, stderr=PIPE, encoding='utf8')
    stdout, stderr = session.communicate()
    #print(stdout, stderr)
    os.chdir(cwd)
    lines = stdout.split("\n")
    return [l.strip().split("\t") for l in lines]





def download_mer():
    pass

