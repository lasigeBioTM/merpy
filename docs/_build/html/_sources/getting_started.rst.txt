

MER is a Named-Entity Recognition tool which given any lexicon and any
input text returns the list of terms recognized in the text, including
their exact location (annotations).

Given an ontology (owl file) MER is also able to link the entities to
their classes.


Dependencies
------------

awk
~~~

MER was developed and tested using the GNU awk (gawk) and grep. If you
have another awk interpreter in your machine, there's no assurance that
the program will work.

For example, to install GNU awk on Ubuntu:

::

    sudo apt-get install gawk

Currently, merpy will not run unless gawk is available.

Installation
------------

.. code:: bash

    pip install merpy

or

.. code:: bash

    python setup.py install

Then you might want to update the MER scripts and download preprocessed
data:

.. code:: python

    >>> import merpy
    >>> merpy.download_mer()
    >>> merpy.download_lexicons()

Basic Usage
-----------

.. code:: python

    >>> import merpy
    >>> merpy.download_lexicons()
    >>> merpy.process_lexicon("hp")
    >>> document = 'Influenza, commonly known as "the flu", is an infectious disease caused by an influenza virus. Symptoms can be mild to severe. The most common symptoms include: a high fever, runny nose, sore throat, muscle pains, headache, coughing, and feeling tired'
    >>> entities = merpy.get_entities(document, "hp")
    >>> print(entities)
    [['111', '115', 'mild', 'http://purl.obolibrary.org/obo/HP_0012825'], ['119', '125', 'severe', 'http://purl.obolibrary.org/obo/HP_0012828'], ['168', '173', 'fever', 'http://purl.obolibrary.org/obo/HP_0001945'], ['214', '222', 'headache', 'http://purl.obolibrary.org/obo/HP_0002315'], ['224', '232', 'coughing', 'http://purl.obolibrary.org/obo/HP_0012735'], ['246', '251', 'tired', 'http://purl.obolibrary.org/obo/HP_0012378'], ['175', '185', 'runny nose', 'http://purl.obolibrary.org/obo/HP_0031417']]
    >>> lexicons = merpy.get_lexicons()
    >>> merpy.show_lexicons()
    lexicons preloaded:
    ['lexicon', 'go', 'cell_line_and_cell_type', 'chebi_lite', 'chemical', 'hp', 'disease', 'wordnet_nouns', 'hpo', 'radlex', 'doid', 'protein', 'hpomultilang', 'tissue_and_organ', 'mirna', 'subcellular_structure']

    lexicons loaded ready to use:
    ['lexicon', 'doid', 'hp']

    lexicons with linked concepts:
    ['doid', 'hp', 'go', 'chebi_lite', 'lexicon']
    >>> merpy.create_lexicon(["gene1", "gene2", "gene3"], "genelist")
    wrote genelist lexicon
    >>> merpy.process_lexicon("genelist")
    >>> merpy.download_lexicon("https://github.com/lasigeBioTM/MER/raw/biocreative2017/data/ChEBI.txt", "chebi")
    wrote chebi lexicon
    >>> merpy.process_lexicon("chebi")
