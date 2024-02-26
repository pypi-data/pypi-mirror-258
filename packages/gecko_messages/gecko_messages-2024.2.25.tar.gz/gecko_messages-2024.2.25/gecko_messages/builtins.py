###############################################
# The MIT License (MIT)
# Copyright (c) 2023 Kevin Walchko
# see LICENSE for full details
##############################################
# -*- coding: utf-8 -*-

complex_types_global = """
[global]
license = '''The MIT License (MIT)
Copyright (c) 2023 Kevin Walchko
see LICENSE for full details
'''
frozen = false
"""

complex_types = [
    """
    [message]
    float-x = 1
    float-y = 1
    float-z = 1
    id = 1
    name = "vec_t"
    """,
    """
    [message]
    float-w = 1
    float-x = 1
    float-y = 1
    float-z = 1
    id = 2
    name = "quat_t"
    """,
    """
    [message]
    vec_t-linear = 1
    vec_t-angular = 1
    id = 3
    name = "twist_t"
    """,
    """
    [message]
    vec_t-force = 1
    vec_t-torque = 1
    id = 4
    name = "wrench_t"
    """,
    """
    [message]
    vec_t-position = 1
    quat_t-orientation = 1
    id = 5
    name = "pose_t"
    """]