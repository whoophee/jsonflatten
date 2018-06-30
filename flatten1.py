import json
from pprint import pprint
filename = "restaurants"


final_data = {}

# Recursive function to flatten
def flatten(obj, indices = [], depth = ()):

    cur_string = '_'.join(depth)

    if not isinstance(obj, (list, dict)):
        return obj

    # non trivial branches for list, dict
    if isinstance(obj, list):

        if not final_data.get(cur_string):
            final_data[cur_string] = []
        current_obj = []

        # TODO : Write exception for trivial arrays

        for index, val in enumerate(obj):
            tmp = None
            # Accomodate mixed arrays and indexing
            try:
                id = val.get('id')
                if id:
                    tmp = flatten(val, indices + [('id', id)], depth)
                else:
                    tmp = flatten(val, indices + [('__index', index)], depth)
            except AttributeError:
                tmp = flatten(val, indices, depth)
            if tmp:
                current_obj.append(tmp)
        final_data[cur_string] = final_data[cur_string] + current_obj
        return None

    if isinstance(obj, dict):
        current_obj = {}
        for name, id in indices:
            current_obj[name] = id
        if not final_data.get(cur_string):
            final_data[cur_string] = []

        for key, val in obj.items():
            # Flatten all child content
            tmp = flatten(val, indices, depth + (key,))
            # Ignore non-trivial children
            if tmp:
                current_obj[key] = tmp
        final_data[cur_string].append(current_obj)

with open("{}.json".format(filename)) as jsonfile:
    json_obj = json.loads(jsonfile.read())
    flatten(json_obj)
    final_data.pop('')
    # TODO : Handle nested indexing
    pprint(final_data)
