import json
import sys

default_file = "restaurants.json"

final_data = {}

# obj : json object to be flattened
# indices : different unique index used to identify current subobject
# depth : tuple of names traversed in original object to reach subobject
def flatten_list(obj, indices, depth):

    cur_string = '_'.join(depth)
    if not final_data.get(cur_string):
        final_data[cur_string] = []
    current_obj = []

    # Return list as is, if it entirely consists of non-dict/non-list contents
    if not any(isinstance(i, (list, dict)) for i in obj):
        return obj

    for index, subobj in enumerate(obj):
        tmp = None
        # Accomodate mixed arrays and indexing
        try:
            id = subobj.get('id')
            if id:
                tmp = flatten(subobj, indices + [('id', id)], depth)
            else:
                tmp = flatten(subobj, indices + [('__index', index)], depth)
        # AttributeError implies the list contains non-dict contents
        # They are not ignored here, to allow reconstruction of original from subfiles.
        except AttributeError:
            tmp = flatten(subobj, indices, depth)
        if tmp:
            current_obj.append(tmp)
    final_data[cur_string] += current_obj

def flatten_dict(obj, indices, depth):
    cur_string = '_'.join(depth)
    current_obj = {}

    # Handle nested indexing (e.g. multiple nested "id" or "__index" fields)
    for name, id in indices:
        if not current_obj.get(name):
            current_obj[name] = id
        else:
            if not isinstance(current_obj[name], list):
                current_obj[name] = (current_obj[name],)
            current_obj[name] += (id,)

    if not final_data.get(cur_string):
        final_data[cur_string] = []

    for field, subobj in obj.items():
        temp_field = field

        ############################################################################
        # RENAMING FIELD NAMES WOULD HIGHLY IMPEDE RECONSTRUCTION OF ORIGINAL FILE #
        ############################################################################

        # truncate last character if current subobject is a list
        # stopgap measure:
        # add "__l" suffix to allow easier reconstruction and lesser
        # chance of overlapping field names.

        if isinstance(subobj, list) and len(field) > 1:
            temp_field = field[:-1]
            # temp_field += '__l'

        # Flatten all child content
        tmp = flatten(subobj, indices, depth + (temp_field,))
        # Ignore non-trivial children
        if tmp:
            current_obj[temp_field] = tmp
    final_data[cur_string].append(current_obj)

# Recursive function to flatten object
def flatten(obj, indices = [], depth = ()):

    if not isinstance(obj, (list, dict)):
        return obj

    if isinstance(obj, list):
        return flatten_list(obj, indices, depth)

    if isinstance(obj, dict):
        return flatten_dict(obj, indices, depth)


def flatten_json(filename):
    json_obj = None
    try:
        with open(filename) as jsonfile:
            json_obj = json.loads(jsonfile.read())
    except:
        print("Error occured in reading file.")

    flatten(json_obj)
    final_data.pop('')

    for field, subobj in final_data.items():
        cur_file = "{}.json".format(field)
        try:
            outfile = open(cur_file,'x')
        except:
            break
        print("Generated {}".format(cur_file))
        json.dump(subobj, outfile)



if __name__ == '__main__':
    # Attempt to read file. Default to restaurants.json
    if len(sys.argv) > 1:
        try:
            flatten_json(sys.argv[1])
        except Exception as e:
            print(e)
    else:
        print("Defaulting to {}".format(default_file))
        flatten_json(default_file)
