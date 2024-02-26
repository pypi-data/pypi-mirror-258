###############################################
# The MIT License (MIT)
# Copyright (c) 2023 Kevin Walchko
# see LICENSE for full details
##############################################
# -*- coding: utf-8 -*-

# from .utils import calc_msg_size
from .utils import parse_global
from .types import var_types
from pathlib import Path
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader


def create_cpp(msg, template="msg.cpp.jinja"):
    tmp_dir = Path(__file__).resolve().parent/"templates"
    # tmp_dir = Path(".").resolve()/"templates"
    # print(tmp_dir)
    env = Environment(loader=FileSystemLoader(tmp_dir))
    tmpl = env.get_template(template)
    info = parse_c(msg)
    content = tmpl.render(info)
    return content

def includes_c(msg):
    """
     'message': {'name': 'quat_t',
             'vars': [Var(type='float', var='w', value=1, array_size=0),
                      Var(type='float', var='x', value=0, array_size=0),
                      Var(type='float', var='y', value=0, array_size=0),
                      Var(type='float', var='z', value=0, array_size=0)]},

    REMOVE: local, global
    REPLACE: c = ['"vec_t"', "<cstdint>"]
    Libraries aren't working right ... not in header
    """
    includes = set()
    for var in msg["message"]["vars"]:
        c = var.complex
        if c is True:
            includes.add(f"#include \"{var.type}.hpp\"")
    return list(includes)

def parse_c(msg):
    """

    """
    # FIXME: limit to 80 cols
    # width = 80

    enums = None
    enums_type = None
    if "enums" in msg:
        enums = msg["enums"]

        enums_type = "uint8_t"
        if "type" in msg["enums"]:
            enums_type = msg["enums"]["type"]

    msg_comments = None
    # if "comments" in msg["message"]:
    #     msg_comments = format_str_width(msg['message']['comments'],'  //',width)

    # _,_,msg_size,_,_,_ = calc_msg_size(msg["message"]["name"], msg["message"]["vars"])
    msginfo = var_types[msg["message"]["name"]]
    msg_size = msginfo.size

    includes = ["#include <cstdint>"]
    includes += includes_c(msg)

    vars = []
    incs = set()
    for v in msg["message"]["vars"]:
        vars.append(v.c_format())

    c_funcs = None
    if "functions" in msg:
        if "c" in msg["functions"]:
            c_funcs = msg["functions"]["c"]

    namespace, license, yivo, mavlink, frozen, msg_id, comments = parse_global(msg, '//')

    if "id" in msg["message"]:
        msg_id = msg["message"]["id"]

    info = {
        "name": msg["message"]["name"], # str
        "vars": vars,                   # list of str
        "includes": includes,           # list
        "comments": comments,           # str - global comments
        "msg_comments": msg_comments,   # str - comment in msg
        "type": "uint8_t",              # str - msg_size
        "functions": c_funcs,           # list of str
        "enums": enums,                 # dict: {name: {var:value, ...}, name:...}
        "enums_type": enums_type,       # str
        "size": msg_size,               # int
        "namespace": namespace,         # str
        "mavlink": mavlink,             # bool
        "yivo": yivo,                   # bool
        "license": license,             # str
        "msg_id": msg_id                # int
    }

    return info