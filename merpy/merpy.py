import os
import sys
import stat
import glob
import zipfile
import shutil
import urllib.request
from subprocess import Popen, PIPE
import pkg_resources as pkg
import requests

mer_path = pkg.resource_filename("merpy", "MER/")


def process_lexicon(lexicon):
    """Preprocess (/generate/load) lexicon, generating index files


    :param lexicon: name of previously downloaded lexicon to be used
    :type lexicon: string

    :Example:

    >>> import merpy
    >>> merpy.process_lexicon("hp")

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
    print(stdout, stderr, file=sys.stderr)
    os.chdir(cwd)


def generate_lexicon(lexicon):
    process_lexicon(lexicon)


def get_entities(text, lexicon):
    """Get entities mention in a text

    :param text: Text to be processed
    :type text: string
    :param lexicon: Lexicon used to get the entities
    :type lexicon: string
    :return: list of entities with index and ontology concept
    :rtype: list

    :Example:

    >>> import merpy
    >>> merpy.process_lexicon("hp")
    >>> document = 'Influenza, commonly known as "the flu", is an infectious disease caused by an influenza virus. Symptoms can be mild to severe. The most common symptoms include: a high fever, runny nose, sore throat, muscle pains, headache, coughing, and feeling tired'
    >>> merpy.get_entities(document, "hp")
    [['111', '115', 'mild', 'http://purl.obolibrary.org/obo/HP_0012825'], \
['246', '251', 'tired', 'http://purl.obolibrary.org/obo/HP_0012378']]
    
    """
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
    """Download latest version of MER from GitHub.
    
    :Example:
        >>> import merpy
        >>> merpy.download_mer()
    
    """

    download_link = "https://github.com/lasigeBioTM/MER/archive/master.zip"
    urllib.request.urlretrieve(download_link, "dishin.zip")[0]
    with zipfile.ZipFile("dishin.zip", "r") as zip_ref:
        zip_ref.extractall()

    bash_scripts = ["get_entities.sh", "get_similarity.sh", "produce_data_files.sh"]
    for script_name in bash_scripts:
        shutil.move("MER-master/" + script_name, mer_path + script_name)
        os.chmod(mer_path + script_name, stat.S_IRWXU)


def create_lexicon_from_ontology(ontology):
    pass


def create_lexicon(entities, name):
    """Create lexicon from list of entities

    :param entities: list of entities
    :type entities: list
    :param name: name of lexicon
    :type name: string


    :Example:
    >>> import merpy
    >>> merpy.create_lexicon(["gene1", "gene2", "gene3"], "genelist")
    wrote genelist lexicon
    >>> merpy.process_lexicon("genelist")
    >>> merpy.get_entities("gene1 and gene2", "genelist")
    [['0', '5', 'gene1'], ['10', '15', 'gene2']]
    """
    with open(mer_path + "/data/" + name + ".txt", "w") as f:
        f.write("\n".join(entities))
    print("wrote {} lexicon".format(name))


def download_lexicon(url, name):
    """Download lexicon from external resource

    :param url: URL to download lexicon
    :type url: string
    :param name: name of lexicon
    :type name: string

    :Example:
        >>> import merpy
        >>> merpy.download_lexicon("https://github.com/lasigeBioTM/MER/raw/biocreative2017/data/ChEBI.txt", "chebi")
        wrote chebi lexicon
        >>> merpy.process_lexicon("chebi")
        >>> merpy.get_entities("caffeine", "chebi")
        [['0', '8', 'caffeine']]
    """
    r = requests.get(url)
    with open(mer_path + "/data/" + name + ".txt", "wb") as f:
        f.write(r.content)
    print("wrote {} lexicon".format(name))


def get_lexicons():
    """Returns list of all lexicons in data directory, as well as pre-processed (loaded) lexicons and lexicons with links file
    
    :return: lists of all lexicons, loaded lexicons and lexicons with entity linking
    :rtype: list

    :Example:
        >>> import merpy
        >>> merpy.get_lexicons()
        (['lexicon', 'go', 'cell_line_and_cell_type', 'chebi_lite', 'chemical', 'hp', 'disease', 'wordnet_nouns', \
'hpo', 'radlex', 'doid', 'genelist', 'chebi', 'protein', 'hpomultilang', 'tissue_and_organ', 'gene', 'mirna', \
'subcellular_structure'], ['gene', 'lexicon', 'chebi', 'doid', 'genelist', 'hp'], \
['doid', 'hp', 'go', 'chebi_lite', 'lexicon'])

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
    """Print lexicon list

    :Example:
    >>> import merpy
    >>> merpy.show_lexicons()
    lexicons preloaded:
    ['lexicon', 'go', 'cell_line_and_cell_type', 'chebi_lite', 'chemical', 'hp', 'disease', 'wordnet_nouns', 'hpo', 'radlex', 'doid', 'genelist', 'chebi', 'protein', 'hpomultilang', 'tissue_and_organ', 'gene', 'mirna', 'subcellular_structure']
    <BLANKLINE>
    lexicons loaded ready to use:
    ['gene', 'lexicon', 'chebi', 'doid', 'genelist', 'hp']
    <BLANKLINE>
    lexicons with linked concepts:
    ['doid', 'hp', 'go', 'chebi_lite', 'lexicon']
    """
    lexicons = get_lexicons()
    print("lexicons preloaded:")
    print(lexicons[0])
    print()
    print("lexicons loaded ready to use:")
    print(lexicons[1])
    print()
    print("lexicons with linked concepts:")
    print(lexicons[2])
