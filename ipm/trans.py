'''
Define the translate functions on:
1. Json file to Threshold object;
2. Threshold object to Json file;
...

'''
import os
import datetime
import json
import logging

def read_file_to_obj(file):
    '''
    Read a JSON file, and store it to a Python Obj
    :param file: a JSON file
    :return: a Python object
    '''
    with open(file, "r") as f:
        data = f.read()
        obj = json.loads(data)

    return obj

def write_obj_to_file(obj, file):
    '''
    Write a Python Obj to a JSON file
    :param obj: a Python object
    :param file: a .JSON file
    :return:
    '''
    with open(file, "w") as f:
        dataString = json.dumps(obj, sort_keys=True, indent=4)
        f.write(dataString)

    return file




