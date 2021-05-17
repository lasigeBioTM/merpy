import merpy
import ssmpy

document = "zoophilia zoophobia zaspopathy"
entities = merpy.get_entities(document, "doid")
print(entities)
print(merpy.get_similarities(entities, 'doid.db'))
