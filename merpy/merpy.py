import os
from subprocess import Popen, PIPE
import pkg_resources as pkg
mer_path = pkg.resource_filename("merpy", "data/MER/")


def generate_lexicon(lexicon):
    cwd = os.getcwd()
    os.chdir(mer_path + "/data/") 
    session = Popen(['../produce_data_files.sh', lexicon], stdout=PIPE, stderr=PIPE, encoding='utf8')
    stdout, stderr = session.communicate()
    print(stdout, stderr)
    os.chdir(cwd)


def get_entities(text, lexicon):
    cwd = os.getcwd()
    os.chdir(mer_path) 
    session = Popen(['./get_entities.sh', text, lexicon], stdout=PIPE, stderr=PIPE, encoding='utf8')
    stdout, stderr = session.communicate()
    #print(stdout, stderr)
    if len(stderr) > 0:
        #TODO: throw exception
        print(stderr) 
    os.chdir(cwd)
    lines = stdout.strip().split("\n")
    return [l.strip().split("\t") for l in lines]


def download_mer():
    pass

