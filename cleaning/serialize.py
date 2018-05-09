# A set of tools to serialize into documents any form of structured JSON-like data

import re
import json
import validators

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Source: https://stackoverflow.com/questions/12507206/python-recommended-way-to-walk-complex-dictionary-structures-imported-from-json

# This code turns a dictionary into a list of paths to leaves
def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in dict_generator(value, [key] + pre):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in dict_generator(v, [key] + pre):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield indict

# Turns a JSON object into a document.
# Just from looking at the result it seems we should filter out:
#  - Empty leaves
#  - Numbers
#  - URL's and emails
#  - Dates?

# Turns a structure into a list of sentences
def struct2sentence(cln):
    # Convert to javascript-style dictionary-array object
    hierarchy = json.loads(json.dumps(cln))

    path_gen = dict_generator(hierarchy)
    sentences = []

    for path in path_gen:
        leaf = path[-1]

        # Do some filtering on the leaves (see below)
        if leaf == '' or leaf == None:
            continue
        if is_number(leaf):
            continue
        if validators.url(leaf):
            continue

        sentence = ' '.join(path)
        
        # Make sentence lowercase and remove periods
        sentence = re.sub(r'[^\s\w]+', ' ', sentence)
        sentences.append(sentence.lower())
    
    return sentences

