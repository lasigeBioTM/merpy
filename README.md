[![Downloads](https://pepy.tech/badge/merpy)](https://pepy.tech/project/merpy)

Use MER scripts inside python.


(from the MER repository)

MER is a Named-Entity Recognition tool which given any lexicon and any input text returns the list of 
terms recognized in the text, including their exact location (annotations).

Given an ontology (owl file) MER is also able to link the entities to their classes.

More information about MER can be found in:
- MER: a Shell Script and Annotation Server for Minimal Named Entity Recognition and Linking, F. Couto and A. Lamurias, Journal of Cheminformatics, 10:58, 2018
[https://doi.org/10.1186/s13321-018-0312-9]
- MER: a Minimal Named-Entity Recognition Tagger and Annotation Server, F. Couto, L. Campos, and A. Lamurias, in BioCreative V.5 Challenge Evaluation, 2017
[https://www.researchgate.net/publication/316545534_MER_a_Minimal_Named-Entity_Recognition_Tagger_and_Annotation_Server]


**NEW**
- Package lexicons202302.tgz is available
- New examples added, namely the ontologies: OSCI, CL, ENVO, and ECTO  
- Docker image available: https://hub.docker.com/r/fjmc/merpy-image
- Package lexicons202103.tgz is available
- Multilingual lexicons using DeCS

## Documentation

https://merpy.readthedocs.io/en/latest/

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
['lexicon', 'bireme_decs_por2020', 'bireme_decs_spa2020', 'wordnet-hyponym', 'radlex', 'doid', 'bireme_decs_eng2020', 'go', 'hp', 'chebi_lite']
lexicons loaded ready to use:
['bireme_decs_por2020', 'chebi_lite', 'hp', 'bireme_decs_spa2020', 'wordnet-hyponym', 'doid', 'lexicon', 'radlex', 'go', 'bireme_decs_eng2020']
lexicons with linked concepts:
['bireme_decs_eng2020', 'doid', 'hp', 'go', 'lexicon', 'bireme_decs_spa2020', 'bireme_decs_por2020', 'radlex', 'chebi_lite']

>>> document = 'Influenza, commonly known as "the flu", is an infectious disease caused by an influenza virus. Symptoms can be mild to severe. The most common symptoms include: a high fever, runny nose, sore throat, muscle pains, headache, coughing, and feeling tired ... Acetylcysteine for reducing the oxygen transport and caffeine to stimulate ... fever, tachypnea ... fiebre, taquipnea ... febre, taquipneia' 
>>> entities = merpy.get_entities(document, "hp") # get_entities_mp uses multiprocessing (set n_cores param)
>>> print(entities)
[['111', '115', 'mild', 'http://purl.obolibrary.org/obo/HP_0012825'], ['119', '125', 'severe', 'http://purl.obolibrary.org/obo/HP_0012828'], ['168', '173', 'fever', 'http://purl.obolibrary.org/obo/HP_0001945'], ['181', '185', 'nose', 'http://purl.obolibrary.org/obo/UBERON_0000004'], ['200', '206', 'muscle', 'http://purl.obolibrary.org/obo/UBERON_0005090'], ['214', '222', 'headache', 'http://purl.obolibrary.org/obo/HP_0002315'], ['224', '232', 'coughing', 'http://purl.obolibrary.org/obo/HP_0012735'], ['246', '251', 'tired', 'http://purl.obolibrary.org/obo/HP_0012378'], ['288', '294', 'oxygen', 'http://purl.obolibrary.org/obo/CHEBI_15379'], ['295', '304', 'transport', 'http://purl.obolibrary.org/obo/GO_0006810'], ['335', '340', 'fever', 'http://purl.obolibrary.org/obo/HP_0001945'], ['342', '351', 'tachypnea', 'http://purl.obolibrary.org/obo/HP_0002789'], ['175', '185', 'runny nose', 'http://purl.obolibrary.org/obo/HP_0031417'], ['187', '198', 'sore throat', 'http://purl.obolibrary.org/obo/HP_0033050']]

>>> entities = merpy.get_entities(document, "bireme_decs_por2020") 
>>> print(entities)
[['0', '9', 'Influenza', 'https://decs.bvsalud.org/ths/?filter=ths_regid&q=D007251'], ['78', '87', 'influenza', 'https://decs.bvsalud.org/ths/?filter=ths_regid&q=D007251'], ['378', '383', 'febre', 'https://decs.bvsalud.org/ths/?filter=ths_regid&q=D005334'], ['385', '395', 'taquipneia', 'https://decs.bvsalud.org/ths/?filter=ths_regid&q=D059246']]

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
wget http://labs.rd.ciencias.ulisboa.pt/dishin/chebi202104.db.gz
gunzip -N chebi202104.db.gz
```

```python
>>> import merpy
>>> merpy.process_lexicon("lexicon")
>>> document = "α-maltose and nicotinic acid was found, but not nicotinic acid D-ribonucleotide"
>>> entities = merpy.get_entities(document, "lexicon") 
>>> merpy.get_similarities(entities, 'chebi.db')
[['0', '9', 'α-maltose', 'http://purl.obolibrary.org/obo/CHEBI_18167', 0.02834388514184269], ['14', '28', 'nicotinic acid', 'http://purl.obolibrary.org/obo/CHEBI_15940', 0.07402224403263755], ['48', '62', 'nicotinic acid', 'http://purl.obolibrary.org/obo/CHEBI_15940', 0.07402224403263755], ['48', '79', 'nicotinic acid D-ribonucleotide', 'http://purl.obolibrary.org/obo/CHEBI_15763', 0.07402224403263755]]

```
