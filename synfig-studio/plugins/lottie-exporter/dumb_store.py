# pylint: disable=line-too-long
"""
Store a value and retrieve it later
"""

def init():
    global store_dict
    store_dict = {}

    global store_next_key
    store_next_key = int()


def put(value):
    global store_next_key
    key = str(store_next_key)
    store_next_key += 1

    global store_dict
    store_dict[key] = value
    return key

def get(key):
    global store_dict
    if key not in store_dict:
        return None
    return store_dict[key]
