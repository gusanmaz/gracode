import os


def get_dirs(path, full=True):
    listing = os.scandir(path)
    dirs = list()
    for entry in listing:
        if entry.is_dir():
            add = entry.name
            if full:
                add = os.path.join(path, add)
            dirs.append(add)
    return dirs


def read_file(path):
    f = open(path)
    contents = f.read()
    f.close()
    return contents


def dict_to_list(dictionary):
    values = list(dictionary.values())
    return values


def filter_by_field(dictionaries, field):
    filtered_list = []
    for dictionary in dictionaries:
        if field in dictionary:
            filtered_list.append(dictionary)
    return filtered_list
