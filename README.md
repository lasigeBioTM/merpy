User MER scripts inside python

```python
>>> import merpy
>>> merpy.generate_lexicon("hp")
>>> document = ""
>>> entities = merpy.get_entities(document, "hp")
```