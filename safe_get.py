

def safe_get(data,*keys,defualt=None,expected_type=None):


    '''
    A Function to safely get data from simple or nested list / dicts.
    Data should be either a list or dict and can provide nested keys
    '''


    current = data

    for key in keys:

        if isinstance(current,dict):
            current = current.get(key)

        elif isinstance(current,list) and isinstance(key,int):
            try:
                current = current[key]
            except IndexError:
                return defualt

        else:
            return defualt

        if current is None:
            return defualt


    if expected_type and current is not None:
        try:
            return expected_type(current)
        except(ValueError,TypeError):
            return defualt

    return current



'''
repos = [
    {"name": "A", "stars": "100", "license": {"name": "MIT"}}, # Normal
    {"name": "B", "stars": 50, "license": None},               # Null license
    {"name": "C"}                                              # Missing keys
]


# For all
for i in range(len(repos)):
    print(safe_get(repos[i],'license','name'))


# For one
print()
print(safe_get(repos,[0],'license'))

'''

