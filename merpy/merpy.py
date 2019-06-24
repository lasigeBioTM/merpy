import os
import sys
import glob
from subprocess import Popen, PIPE
import pkg_resources as pkg
import requests

mer_path = pkg.resource_filename("merpy", "MER/")


def generate_lexicon(lexicon):
    """
    Preprocess (/generate/load) lexicon
    """
    cwd = os.getcwd()
    os.chdir(mer_path + "/data/")
    if sys.version_info[0] == 3 and sys.version_info[1] > 5:
        session = Popen(
            ["../produce_data_files.sh", lexicon],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
    else:
        session = Popen(
            ["../produce_data_files.sh", lexicon],
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True,
        )
    stdout, stderr = session.communicate()
    print(stdout, stderr)
    os.chdir(cwd)


def get_entities(text, lexicon):
    cwd = os.getcwd()
    os.chdir(mer_path)
    if sys.version_info[0] == 3 and sys.version_info[1] > 5:
        session = Popen(
            ["./get_entities.sh", text, lexicon],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
    else:
        session = Popen(
            ["./get_entities.sh", text, lexicon],
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True,
        )
    stdout, stderr = session.communicate()
    # print(stdout, stderr)
    if len(stderr) > 0:
        # TODO: throw exception
        print(stderr)
    os.chdir(cwd)
    lines = stdout.strip().split("\n")
    return [l.strip().split("\t") for l in lines]


def download_mer():
    pass


def download_lexicon(url, name):
    r = requests.get(url)
    with open(mer_path + "/data/" + name + ".txt", "wb") as f:
        f.write(r.content)
    print("wrote {} lexicon".format(name))


def get_lexicons():
    """
    Returns list of all lexicons in data directory, as well as pre-processed (loaded) lexicons and lexicons with links file
    """
    all_lexicons, loaded_lexicons, links_lexicons = [], [], []
    files = os.listdir(mer_path + "/data/")

    for f in files:
        if f.endswith(".txt") and not (
            f.endswith("_word2.txt")
            or f.endswith("_words.txt")
            or f.endswith("_word1.txt")
            or f.endswith("_links.tsv")
            or f.endswith("_words2.txt")
        ):
            all_lexicons.append(".".join(f.split(".")[:-1]))

    for f in files:
        if f.endswith("_words2.txt"):  # TODO: verify if all files exist
            loaded_lexicons.append("_".join(f.split("_")[:-1]))

    for f in files:
        if f.endswith("_links.tsv"):
            links_lexicons.append("_".join(f.split("_")[:-1]))
    return all_lexicons, loaded_lexicons, links_lexicons


def show_lexicons():
    lexicons = get_lexicons()
    print("lexicons preloaded:")
    print(lexicons[0])
    print()
    print("lexicons loaded ready to use:")
    print(lexicons[1])
    print()
    print("lexicons with linked concepts:")
    print(lexicons[2])
