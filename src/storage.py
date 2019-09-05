# Auracoin
# 
# Copyright (C) Aurora Enterprise. All Rights Reserved.
# 
# https://aur.xyz
# Licensed by the Auracoin Open-Source Licence, which can be found at LICENCE.md.

import os
import pickle
import configparser

CONFIG_FOLDER = os.path.join(os.path.expanduser("~"), ".auracoin")
CONFIG_FILE = os.path.join(CONFIG_FOLDER, "config.auc")

def saveObject(data, name):
    file = open(os.path.join(CONFIG_FOLDER, name + ".auo"), "wb")

    pickle.dump(data, file)
    file.close()

def openObject(name):
    file = open(os.path.join(CONFIG_FOLDER, name + ".auo"), "rb")
    data = pickle.load(file)

    file.close()

    return data

def setConfigItem(section, name, data):
    config = configparser.ConfigParser()

    config.read(CONFIG_FILE)

    if not config.has_section(section):
        config.add_section(section)

    config.set(section, name, data)

    file = open(CONFIG_FILE, "w")

    config.write(file)
    file.close()

def getConfigItem(section, name, dataType = "string"):
    config = configparser.ConfigParser()

    config.read(CONFIG_FILE)

    if dataType == "string":
        return config.get(section, name)
    elif dataType == "bool":
        return config.getboolean(section, name)
    elif dataType == "int":
        return config.getint(section, name)
    elif dataType == "float":
        return config.getfloat(section, name)
    else:
        raise TypeError("data type not allowed")