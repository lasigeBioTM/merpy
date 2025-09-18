[![Downloads](https://pepy.tech/badge/merpy)](https://pepy.tech/project/merpy)

# MER (Minimal Named-Entity Recognizer) inside Python

https://pypi.org/project/merpy

MER is a Named-Entity Recognition tool that identifies terms from any lexicon within input text, providing their exact locations (annotations). 
It can also link recognized entities to their respective classes when provided with an ontology (OWL file).

A demo is available at: [MER Demo](https://labs.rd.ciencias.ulisboa.pt/mer/)

[Package](https://pypi.org/project/merpy/)

[Package documentation](https://merpy.readthedocs.io/en/latest/)


## New Stuff

### 2025
- **LEXICONS**: Package [here](https://labs.rd.ciencias.ulisboa.pt/mer/lexicons202506.tgz) is available.
  
### 2024
- **LEXICONS**: Package [here](https://labs.rd.ciencias.ulisboa.pt/mer/lexicons202407.tgz) is available.
- **COMMENTS**: More comments were added to the scripts to improve readability.

### 2023
- **ONTOLOGIES**: New examples added, namely the ontologies: OSCI, CL, ENVO, and ECTO.

### 2021
- **DOCKER**: Image available: [fjmc/mer-image](https://hub.docker.com/r/fjmc/mer-image).
- **MULTILINGUAL**: English, Spanish, and Portuguese lexicons using DeCS.
- **PYTHON**: Interface: [lasigeBioTM/merpy](https://github.com/lasigeBioTM/merpy/).
- **SIMILARITY**: `get_similarities.sh` finds the most similar term also recognized. See [here](https://github.com/lasigeBioTM/MER#Similarity).

## Dependencies

### awk

MER was developed and tested using the GNU awk (gawk) and grep. If you have another awk interpreter in your machine, there's no assurance that the program will work.

For example, to install GNU awk on Ubuntu:

```bash
sudo apt-get install gawk
```

### ssmpy

To calculate similarities between the recognized entities

```bash
pip install ssmpy
```


## Installation
```bash
pip install merpy
```
or

```bash
python setup.py install
```

Then you might want to update the MER scripts and download preprocessed data:
```python
>>> import merpy
>>> merpy.download_mer()
>>> merpy.download_lexicons()
```


## Basic Usage

```python
>>> import merpy
>>> merpy.download_lexicons()
>>> lexicons = merpy.get_lexicons()
>>> merpy.show_lexicons()
lexicons preloaded:
['bireme_decs_spa2024', 'bireme_decs_eng2020', 'bireme_decs_por2020', 'hp', 'bireme_decs_spa2020', 'radlex', 'doid', 'lexicon', 'ecto', 'cl', 'osci', 'envo', 'wordnet-hyponym', 'genelist', 'go', 'bireme_decs_eng2024', 'bireme_decs_por2024', 'chebi_lite']
lexicons loaded ready to use:
['bireme_decs_por2020', 'osci', 'bireme_decs_eng2020', 'go', 'cl', 'bireme_decs_spa2024', 'bireme_decs_spa2020', 'doid', 'bireme_decs_eng2024', 'bireme_decs_por2024', 'chebi_lite', 'lexicon', 'wordnet-hyponym', 'ecto', 'envo', 'radlex', 'hp']
lexicons with linked concepts:
['go', 'bireme_decs_eng2024', 'envo', 'cl', 'ecto', 'doid', 'osci', 'bireme_decs_spa2020', 'bireme_decs_por2024', 'bireme_decs_spa2024', 'bireme_decs_eng2020', 'bireme_decs_por2020', 'lexicon', 'radlex', 'chebi_lite', 'hp']

>>> document = 'Influenza, commonly known as "the flu", is an infectious disease caused by an influenza virus. Symptoms can be mild to severe. The most common symptoms include: a high fever, runny nose, sore throat, muscle pains, headache, coughing, and feeling tired ... Acetylcysteine for reducing the oxygen transport and caffeine to stimulate ... fever, tachypnea ... fiebre, taquipnea ... febre, taquipneia' 
>>> entities = merpy.get_entities(document, "hp") # get_entities_mp uses multiprocessing (set n_cores param)
>>> print(entities)
[['111', '115', 'mild', 'http://purl.obolibrary.org/obo/HP_0012825'], ['119', '125', 'severe', 'http://purl.obolibrary.org/obo/HP_0012828'], ['168', '173', 'fever', 'http://purl.obolibrary.org/obo/HP_0001945'], ['175', '185', 'runny nose', 'http://purl.obolibrary.org/obo/HP_0031417'], ['181', '185', 'nose', 'http://purl.obolibrary.org/obo/UBERON_0000004'], ['187', '198', 'sore throat', 'http://purl.obolibrary.org/obo/HP_0033050'], ['200', '206', 'muscle', 'http://purl.obolibrary.org/obo/UBERON_0005090'], ['214', '222', 'headache', 'http://purl.obolibrary.org/obo/HP_0002315'], ['224', '232', 'coughing', 'http://purl.obolibrary.org/obo/HP_0012735'], ['246', '251', 'tired', 'http://purl.obolibrary.org/obo/HP_0012378'], ['288', '294', 'oxygen', 'http://purl.obolibrary.org/obo/CHEBI_15379'], ['288', '304', 'oxygen transport', 'http://purl.obolibrary.org/obo/GO_0015671'], ['295', '304', 'transport', 'http://purl.obolibrary.org/obo/GO_0006810'], ['335', '340', 'fever', 'http://purl.obolibrary.org/obo/HP_0001945'], ['342', '351', 'tachypnea', 'http://purl.obolibrary.org/obo/HP_0002789']]

>>> entities = merpy.get_entities(document, "bireme_decs_por2024") 
>>> print(entities)
[['378', '383', 'febre', 'https://decs.bvsalud.org/ths/?filter=ths_regid&q=D005334'], ['385', '395', 'taquipneia', 'https://decs.bvsalud.org/ths/?filter=ths_regid&q=D059246']]

>>> merpy.create_lexicon(["gene1", "gene2", "gene3"], "genelist")
wrote genelist lexicon
>>> merpy.process_lexicon("genelist")
>>> merpy.delete_lexicon("genelist")
deleted genelist lexicon
>>> merpy.download_lexicon("https://github.com/lasigeBioTM/MER/raw/biocreative2017/data/ChEBI.txt", "chebi")
wrote chebi lexicon
>>> merpy.process_lexicon("chebi")
```

## Semantic Similarities 

```bash
wget http://labs.rd.ciencias.ulisboa.pt/dishin/chebi202506.db.gz
gunzip -N chebi202506.db.gz
```

```python
>>> import merpy
>>> merpy.process_lexicon("lexicon")
>>> document = "α-maltose and nicotinic acid was found, but not nicotinic acid D-ribonucleotide"
>>> entities = merpy.get_entities(document, "lexicon") 
>>> merpy.get_similarities(entities, 'chebi.db')
[['0', '9', 'α-maltose', 'http://purl.obolibrary.org/obo/CHEBI_18167', 0.02558388153790472], ['14', '28', 'nicotinic acid', 'http://purl.obolibrary.org/obo/CHEBI_15940', 0.07797333766146208], ['48', '62', 'nicotinic acid', 'http://purl.obolibrary.org/obo/CHEBI_15940', 0.07797333766146208], ['48', '79', 'nicotinic acid D-ribonucleotide', 'http://purl.obolibrary.org/obo/CHEBI_15763', 0.07797333766146208]]

```
