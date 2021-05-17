import merpy
import ssmpy
import urllib.request

# Download the Human Disease Ontology OWL file
doid_link='http://purl.obolibrary.org/obo/doid.owl'
with urllib.request.urlopen(doid_link) as response, open('doid.owl', 'wb') as out_file:
    data = response.read() 
    out_file.write(data)

ssmpy.create_semantic_base("doid.owl", "doid.db", "http://purl.obolibrary.org/obo/", "http://www.w3.org/2000/01/rdf-schema#subClassOf", '')
ssmpy.semantic_base("doid.db")

merpy.download_lexicon(doid_link,"doid","owl")
merpy.process_lexicon("doid","owl")
document = "zoophilia zoophobia zaspopathy"
entities = merpy.get_entities(document, "doid")
print(entities)
print(merpy.get_similarities(entities, 'doid.db'))
