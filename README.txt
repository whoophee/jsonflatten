USAGE:

flatten.py [json_file] [-suffix]

Optional arguments:
json_file : The json file to be flattened.
-suffix : Suffixes list fields with '__l' instead of singularizing. Requires json_file to be specified.


FEATURES:

1.) Nesting depth unrestricted.

2.) Nested indexing allows the resultant objects to be uniquely identifiable.
    e.g.
    input : hotels.json
    {
      "hotel":
      [
        {
          "id": "abc",
          "name": "ABC Hotel"
          "foods":[{"id": "123", "name": "food1"}]
        }
      ]
    }
    output :
    hotel.json
    [{"id": "abc","name":"ABC Hotel"}]

    hotel_food.json
    [{"id": ["abc", "123"], "name": "food1"}]

3.) Specify index and default index fields.

KNOWN PROBLEMS:

1.) The deliverables require singularizing field names which cannot
    be generalized to all cases. (e.g. fields having -ies plural).

2.) Singularizing can also cause conflicts between field names.
    'https://s3-us-west-2.amazonaws.com/datacoral.codex/startups.json' contains
    two independent nested fields 'acquisition' and 'acquisitions', both of
    which would result in the same resultant file name. A simple workaround
    is to add an '__l' suffix to list based files (instead of singularizing).
    This workaround requires -suffix flag.
