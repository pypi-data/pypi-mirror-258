###############################################
# The MIT License (MIT)
# Copyright (c) 2023 Kevin Walchko
# see LICENSE for full details
##############################################
# -*- coding: utf-8 -*-
try:
    import tomllib
except ImportError:
    import tomlkit as tomllib

from pathlib import Path
from .builtins import *
from .types import *


def var_fix(data):
    """
    format variables in message properly from the TOML template
    float-x=1 => float x
    float-x=3 => float[3] x
    """
    # print(data)

    vars = []
    key_remove = []

    defaults = None
    if "defaults" in data["message"]:
        defaults = data["message"]["defaults"]
        data["message"].pop("defaults")

    for k,val in data["message"].items():
        try:
            # there are some keys that are not variable types
            # and we are just protecting them here
            if k == "id":
                continue
            if k == "name":
                continue

            key_remove.append(k)

            type, var = k.split('-')
            array_size = int(val)

            if type == "vec_t":
                v = Vec(var, array_size)
            elif type == "quat_t":
                v = Quat(var, array_size)
            elif type == "twist_t":
                v = Twist(var, array_size)
            elif type == "wrench_t":
                v = Wrench(var, array_size)
            elif type == "pose_t":
                v = Pose(var, array_size)
            elif type.find("int") > -1 or type == "float" or type == "double":
                v = Scalar(var, type, array_size)
            else:
                # raise Exception(f"'{type}' is unknown")
                v = Complex(var, type, array_size)

            if defaults:
                if v.variable in defaults:
                    v.default = defaults[v.variable]

            # print(v)

            vars.append(v)
        except ValueError:
            continue

    # Add in new namedtuple Var array
    data["message"]["vars"] = vars

    # remove old keys that were replaced above with namedtuple code
    for k in key_remove:
        data["message"].pop(k)

    return data

def read_toml(file):
    """
    Read toml file and return a dict
    """
    path = Path(file)
    with path.open("rb") as f:
        txt = read(f)

    return read_tomls(txt)

def read_tomls(txt):
    """
    Read toml string and return dict
    """
    data = tomllib.loads(txt)

    if "message" in data:
        data = var_fix(data)
        update_var_types(data)

    return data

def read_folder(dir):
    """
    Read a message folder and return a dict. It is expected each
    message is in an individual toml file. Optionally there can
    be a global.toml file (all lower case) that contains info
    across each message."""
    data_files = []
    p = Path(dir).glob('*.toml')
    files = [x for x in p if x.is_file()]

    # handle global file ------------------------------
    globalFile = False
    gf = Path(dir) / "global.toml"
    gData = {"global": None}
    if gf in files:
        gData = read_toml(gf)
        globalFile = True
        files.remove(gf)

    if "wrap_width" not in gData["global"]:
        gData["global"]["wrap_width"] = 70

    # handle builtins ----------------------------------
    for f in complex_types:
        gc = read_tomls(complex_types_global)
        for key in ["namespace","wrap_width","comments","serialization"]:
            if key in gData["global"]:
                gc[key] = gData["global"][key]
        data = read_tomls(f) | gc
        data_files.append(data)

    # process messages ---------------------------------
    for f in files:
        data = read_toml(f) | gData
        data_files.append(data)
    return data_files

def write_file(filename, content):
    """
    Simple writes content to filename
    """
    if not isinstance(filename, Path):
        filename = Path(filename)

    try:
        with filename.open("w", encoding="utf-8") as fd:
            fd.write(content)
        # print(f"Wrote File: {filename}")
        return True
    except:
        # print(f"Failed to write File: {filename}")
        return False