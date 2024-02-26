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

def create_python(msg, template="msg.py.jinja"):
    """
    Creates a python file for a message from templates found in
    the template_path
    """
    tmp_dir = Path(__file__).resolve().parent/"templates"
    # tmp_dir = Path(".").resolve()/"templates"
    env = Environment(loader=FileSystemLoader(tmp_dir))
    tmpl = env.get_template(template)
    info = parse_python(msg)
    content = tmpl.render(info)
    return content

def includes_python(msg):
    """
    Formats library imports for a python message
    """
    includes = set()
    for var in msg["message"]["vars"]:
        c = var.complex
        if c is True:
            includes.add(f"from .{var.type} import {var.type}")
    return list(includes)

def parse_python(msg):
    """
    Parses a message and returns a dict containing the information needed
    to generate a python file for the message
    """
    # FIXME: limit to 80 cols
    # width = 70

    comments = None
    if "comments" in msg:
        comments = format_str_width(msg["comments"],'#',width)

    enums = None
    if "enums" in msg:
        enums = msg["enums"]

    msg_comments = None
    # if "comments" in msg["message"]:
    #     msg_comments = format_str_width(msg['message']['comments'],'    #',width)


    # _,_,msg_size,format,_,_ = calc_msg_size(msg["message"]["name"], msg["message"]["vars"])
    msginfo = var_types[msg["message"]["name"]]
    msg_size = msginfo.size
    format = msginfo.fmt

    vars = []
    for v in msg["message"]["vars"]:
        vars.append(v.py_format())

    includes = []
    includes += includes_python(msg)

    funcs = None
    if "functions" in msg and "python" in msg["functions"]:
        funcs = msg["functions"]["python"]

    namespace, license, yivo, mavlink, frozen, msg_id, comments = parse_global(msg, '#')

    if "id" in msg["message"]:
        msg_id = msg["message"]["id"]

    info = {
        "name": msg["message"]["name"],  # str
        "vars": vars,                    # list of str
        "includes": includes,            # list
        "comments": comments,            # str - global comments
        "msg_comments": msg_comments,    # str - comment in msg
        "functions": funcs,              # list of str
        "enums": enums,                  # dict: {name: {var:value, ...}, name:...}
        "msg_size": msg_size,            # int
        "namespace": namespace,          # str
        "mavlink": mavlink,              # bool
        "yivo": yivo,                    # bool
        "license": license,              # str
        "msg_id": msg_id,                # int
        "format": format,                # str
        "frozen": frozen,                # bool
    }

    return info
