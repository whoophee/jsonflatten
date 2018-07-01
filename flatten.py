import json
import sys
import testdata
import unittest

SUFFIX = False

class Flattener:
    # obj : json object to be flattened
    # indices : combinatin of indices used to identify current subobject
    # depth : tuple of names traversed in original object to reach subobject
    def _flatten_list(self, obj, indices, depth):

        cur_string = '_'.join(depth)
        if not self._data.get(cur_string):
            self._data[cur_string] = []
        current_obj = []

        # Return list as is, if it entirely consists of non-dict/non-list contents
        if not any(isinstance(i, (list, dict)) for i in obj):
            return obj

        for index, subobj in enumerate(obj):
            tmp = None
            # Accomodate mixed arrays and indexing
            try:
                id = subobj.get(self._index)
                if id:
                    tmp = self._flatten(subobj, indices + [(self._index, str(id))], depth)
                else:
                    tmp = self._flatten(subobj, indices + [(self._default_index, str(index))], depth)
            # AttributeError implies the list contains non-dict contents
            # They are not ignored here, to allow reconstruction of original from subfiles.
            except AttributeError:
                tmp = self._flatten(subobj, indices, depth)
            if tmp:
                current_obj.append(tmp)
        self._data[cur_string] += current_obj

    def _flatten_dict(self, obj, indices, depth):
        cur_string = '_'.join(depth)
        current_obj = {}

        # Handle nested "id"/"__index" fields
        for name, id in indices:
            if not current_obj.get(name):
                current_obj[name] = id
            else:
                if not isinstance(current_obj[name], list):
                    current_obj[name] = [current_obj[name]]
                current_obj[name].append(id)

        if not self._data.get(cur_string):
            self._data[cur_string] = []

        for field, subobj in obj.items():
            if field in [self._index, self._default_index]:
                continue
            temp_field = field

            # truncate trailing character if current subobject is a list
            # stopgap measure:
            # Use "__l" suffix for lesser chance of overlapping field names.
            if isinstance(subobj, list) and len(field) > 1 and field[-1] == 's':
                if not SUFFIX:
                    temp_field = field[:-1]
                else:
                    temp_field += '__l'

            # Flatten all child content
            tmp = self._flatten(subobj, indices, depth + (temp_field,))
            # Ignore non-trivial children
            if tmp:
                current_obj[temp_field] = tmp
        self._data[cur_string].append(current_obj)

    # Recursive function to flatten object
    def _flatten(self, obj, indices = [], depth = ()):

        if not isinstance(obj, (list, dict)):
            return obj

        if isinstance(obj, list):
            return self._flatten_list(obj, indices, depth)

        if isinstance(obj, dict):
            return self._flatten_dict(obj, indices, depth)

    def get_flattened(self, json_obj):
        self._data = {'':None}
        self._flatten(json_obj)
        self._data.pop('')
        return self._data

    # allows specifying name used for index fields
    def __init__(self, primary_index = 'id', unnamed_index = 'index'):
        self._index = primary_index
        self._default_index = '__{}'.format(unnamed_index)


def split_to_file(sol):
    for field, subobj in sol.items():
        cur_file = "{}.json".format(field)
        try:
            outfile = open(cur_file,'x')
            json.dump(subobj, outfile)
            print("Generated {}".format(cur_file))
        except Exception as e:
            print(e)
        

def flatten_json(filename):
    obj = None
    try:
        with open(filename) as jsonfile:
            obj = json.loads(jsonfile.read())
    except Exception as e:
        print(e)
    f = Flattener()
    sol = f.get_flattened(obj)
    split_to_file(sol)

class TestUM(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_1(self):
        f = Flattener()
        self.assertEqual( f.get_flattened(testdata.test1), testdata.sol1)
    def test_2(self):
        f = Flattener()
        self.assertEqual( f.get_flattened(testdata.test2), testdata.sol2)
    def test_3(self):
        f = Flattener()
        self.assertEqual( f.get_flattened(testdata.test3), testdata.sol3)

if __name__ == '__main__':
    # argparse is overkill for 2 arguments
    if len(sys.argv) > 1:
        try:
            if sys.argv[2] == '-suffix':
                SUFFIX = True
        except:
            pass
        try:
            flatten_json(sys.argv[1])
        except Exception as e:
            print(e)
    else:
        if not SUFFIX:
            unittest.main()
