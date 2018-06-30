import json
from pprint import pprint
filename = "restaurants"


class Schema:

    def add_undiscovered(self, key, val):
        if not self.types.get(key):
            self.types[key] = val

    def generate_types(self, obj, key = ()):
        if isinstance(obj, dict):
            self.add_undiscovered(key, "dict")

            for childkey, val in obj.items():
                self.generate_types(val, key + (childkey, ))

        elif isinstance(obj, list):
            self.add_undiscovered(key, "list")
            for val in obj:
                self.generate_types(val, key)
        else:
            self.add_undiscovered(key, "elem")

    def generate_objects(self, obj):


    def __init__(self, json_obj):
        self.types = {}
        self.generate_types(json_obj)
        self.types.pop(())

        schema = {}
        for key, val in self.types.items():
            if val in ("list", "dict"):
                schema[key] = {'children': []}

            if val is "list":


        pprint(schema)
        # for key, val in self.types.items():
        #     key.split('_')







with open("{}.json".format(filename)) as jsonfile:
    json_obj = json.loads(jsonfile.read())
    s = Schema(json_obj)
