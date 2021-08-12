"""Module to aid in storing and loading data from files.

Written by Aaron Young.
"""
import pickle
import json_tricks as json
import os
import sys

def add_extension(path, ext):
    if not os.path.splitext(path)[1] == ext:
        path += ext
    return path

def execute_if_missing(filename, function, *args, **kwargs):
    """Execute method if output file is missing."""
    if not os.path.exists(filename):
        function(*args, **kwargs)


def read_or_new_pickle(filename, value, *args, **kwargs):
    """Read or create a new pickle file and return the data."""
    data = None
    filename = add_extension(filename, '.pkl')
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    if os.path.isfile(filename):
        # If file had been created, but is empty return None since another process
        # could be writing to it.
        if os.path.getsize(filename) > 0:
            with open(filename, "rb") as f:
                try:
                    data = pickle.load(f)
                except Exception as e:
                    print(e)
                    raise e
    else:
        # open(filename, "ab").close()
        if callable(value):
            data = value(*args, **kwargs)
        else:
            data = value
        with open(filename, "wb") as f:
            pickle.dump(data, f)
    return data


def save_pickle(filename, data, override=True):
    """Save data to a pickle."""
    filename = add_extension(filename, '.pkl')
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    if override == False:
        filename = add_unique_postfix(filename)

    with open(filename, "wb") as f:
        pickle.dump(data, f)

    return filename


def read_or_new_txt(filename, value, *args, **kwargs):
    """Read or create a new text file and return the data."""
    data = None
    filename = add_extension(filename, '.txt')
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    if os.path.isfile(filename):
        # If file had been created, but is empty return None since another process
        # could be writing to it.
        if os.path.getsize(filename) > 0:
            with open(filename, "r") as f:
                try:
                    data = f.read()
                except Exception as e:
                    print(e)
                    raise e
    else:
        # open(filename, "ab").close()
        if callable(value):
            data = value(*args, **kwargs)
        else:
            data = value
        with open(filename, "w") as f:
            f.write(data)
    return data


def save_txt(filename, data, override=True):
    """Save data to a text file."""
    filename = add_extension(filename, '.txt')
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    if override == False:
        filename = add_unique_postfix(filename)

    with open(filename, "w") as f:
        f.write(data)

    return filename


def read_or_new_json(filename, value, *args, **kwargs):
    """Read or create a new json file and return the data."""
    data = None
    filename = add_extension(filename, '.json')
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    if os.path.isfile(filename):
        # If file had been created, but is empty return None since another process
        # could be writing to it.
        if os.path.getsize(filename) > 0:
            with open(filename, "r") as f:
                try:
                    data = json.load(f, preserve_order=False)
                except Exception as e:
                    print(e)
                    raise e
    else:
        if callable(value):
            data = value(*args, **kwargs)
        else:
            data = value
        with open(filename, "w") as f:
            json.dump(data, f, indent=4, separators=(',', ': '), sort_keys=True, allow_nan=True)
    return data


def save_json(filename, data, override=True):
    """Save data to a json."""
    filename = add_extension(filename, '.json')
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    if override == False:
        filename = add_unique_postfix(filename)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4, separators=(',', ': '), sort_keys=True, allow_nan=True)

    return filename


def add_unique_postfix(filename):
    """Add postfix to a filename to make it unique."""
    if not os.path.exists(filename):
        return filename

    path, name = os.path.split(filename)
    name, ext = os.path.splitext(name)

    make_filename = lambda i: os.path.join(path, '{}_{}{}'.format(name, i, ext))

    for i in range(1, sys.maxsize):
        unique_filename = make_filename(i)
        if not os.path.exists(unique_filename):
            return unique_filename

    return None


def read_all_data_from_folder(path):
    """Read all the data from a results directory recursively and return a list of all the data."""
    data = []

    # Loop through all files recursively
    for foldername, subfolders, filenames in os.walk(path):

        # Loop though each file
        for filename in filenames:
            name, ext = os.path.splitext(filename)

            filepath = os.path.join(foldername, filename)
            if ext == '.txt':
                with open(filepath, "r") as f:
                    data.append(f.readlines())
            elif ext == '.json':
                with open(filepath, "r") as f:
                    data.append(json.load(f, preserve_order=False))
            elif ext == '.pkl':
                with open(filepath, "rb") as f:
                    data.append(pickle.load(f))

    return data
