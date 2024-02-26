###############################################
# The MIT License (MIT)
# Copyright (c) 2023 Kevin Walchko
# see LICENSE for full details
##############################################
# -*- coding: utf-8 -*-
import sys
from collections import namedtuple

Var = namedtuple("Var","type var value array_size")

drange = namedtuple("drange","min max")
dfprange = namedtuple("drange","fracbit min max res")

def irange(bits, signed):
    """Integer"""
    if signed:
        return drange(-2**(bits-1),2**(bits-1)-1)
    return drange(0,2**bits-1)

def fltrange(double=True):
    """Floating point"""
    return drange(1.175494351e-38,3.402823466e+38)

def dblrange():
    """Floating point"""
    return drange(sys.float_info.min,sys.float_info.max)

def fprange(frac):
    """Fixed Point"""
    whole = 32 - frac
    scale = 1.0 / (2**frac)
    minfp = -2**(whole-1)
    maxfp = 2**(whole-1) - scale
    return dfprange(frac, minfp, maxfp, scale)

# c - c type name
# py - python type name
# fmt - pack/unpack
# complex - non-standard data type
VarInfo = namedtuple("VarInfo","c py size fmt complex default")

var_types = {
    # Standard scalar types --------------------------------------------------------
    "char":   VarInfo("char",     "str",   1, "B", False, 0),
    "uint8":  VarInfo("uint8_t",  "int",   1, "B", False, 0),
    "uint16": VarInfo("uint16_t", "int",   2, "H", False, 0),
    "uint32": VarInfo("uint32_t", "int",   4, "I", False, 0),
    "uint64": VarInfo("uint64_t", "int",   8, "Q", False, 0),
    "int8":   VarInfo("int8_t",   "int",   1, "b", False, 0),
    "int16":  VarInfo("int16_t",  "int",   2, "h", False, 0),
    "int32":  VarInfo("int32_t",  "int",   4, "i", False, 0),
    "int64":  VarInfo("int64_t",  "int",   8, "q", False, 0),
    "float":  VarInfo("float",    "float", 4, "f", False, 0.0),
    "double": VarInfo("double",   "float", 8, "d", False, 0.0),
    # ROS inspired messages -------------------------------------------------------
    "vec_t":    VarInfo("vec_t",    "vec_t",    12, "3f", True, [0,0,0]), # [x y z]
    "quat_t":   VarInfo("quat_t",   "quat_t",   16, "4f", True, [1,0,0,0]), # [w x y z]
    "twist_t":  VarInfo("twist_t",  "twist_t",  24, "6f", True, [0,0,0,0,0,0]), # [linear, angular]
    "wrench_t": VarInfo("wrench_t", "wrench_t", 24, "6f", True, [0,0,0,0,0,0]), # [force, torque]
    "pose_t":   VarInfo("pose_t",   "pose_t",   28, "7f", True, [0,0,0,1,0,0,0]), # [position, attitude]
}

# VarInfo = namedtuple("VarInfo","c py size fmt complex")

# var_types = {
#     # Standard scalar types --------------------------------------------------------
#     "char":   VarInfo("char",     "str",   1, "B", False),
#     "uint8":  VarInfo("uint8_t",  "int",   1, "B", False),
#     "uint16": VarInfo("uint16_t", "int",   2, "H", False),
#     "uint32": VarInfo("uint32_t", "int",   4, "I", False),
#     "uint64": VarInfo("uint64_t", "int",   8, "Q", False),
#     "int8":   VarInfo("int8_t",   "int",   1, "b", False),
#     "int16":  VarInfo("int16_t",  "int",   2, "h", False),
#     "int32":  VarInfo("int32_t",  "int",   4, "i", False),
#     "int64":  VarInfo("int64_t",  "int",   8, "q", False),
#     "float":  VarInfo("float",    "float", 4, "f", False),
#     "double": VarInfo("double",   "float", 8, "d", False),
#     # ROS inspired messages -------------------------------------------------------
#     "vec_t":    VarInfo("vec_t",    "vec_t",    12, "3f", True), # [x y z]
#     "quat_t":   VarInfo("quat_t",   "quat_t",   16, "4f", True), # [w x y z]
#     "twist_t":  VarInfo("twist_t",  "twist_t",  24, "6f", True), # [linear, angular]
#     "wrench_t": VarInfo("wrench_t", "wrench_t", 24, "6f", True), # [force, torque]
#     "pose_t":   VarInfo("pose_t",   "pose_t",   28, "7f", True), # [position, attitude]
# }

# VarInfo = namedtuple("VarInfo","c py size fmt complex range")

# var_types = {
#     # Standard scalar types --------------------------------------------------------
#     "char":   VarInfo("char",     "str",   1, "B", False, irange(8,False)),
#     "uint8":  VarInfo("uint8_t",  "int",   1, "B", False, irange(8,False)),
#     "uint16": VarInfo("uint16_t", "int",   2, "H", False, irange(16,False)),
#     "uint32": VarInfo("uint32_t", "int",   4, "I", False, irange(32,False)),
#     "uint64": VarInfo("uint64_t", "int",   8, "Q", False, irange(64,False)),
#     "int8":   VarInfo("int8_t",   "int",   1, "b", False, irange(8,True)),
#     "int16":  VarInfo("int16_t",  "int",   2, "h", False, irange(16,True)),
#     "int32":  VarInfo("int32_t",  "int",   4, "i", False, irange(32,True)),
#     "int64":  VarInfo("int64_t",  "int",   8, "q", False, irange(64,True)),
#     "float":  VarInfo("float",    "float", 4, "f", False, fltrange()),
#     "double": VarInfo("double",   "float", 8, "d", False, dblrange()),
#     # ROS inspired messages -------------------------------------------------------
#     "vec_t":    VarInfo("vec_t",    "vec_t",    12, "3f", True, 0), # [x y z]
#     "quat_t":   VarInfo("quat_t",   "quat_t",   16, "4f", True, 0), # [w x y z]
#     "twist_t":  VarInfo("twist_t",  "twist_t",  24, "6f", True, 0), # [linear, angular]
#     "wrench_t": VarInfo("wrench_t", "wrench_t", 24, "6f", True, 0), # [force, torque]
#     "pose_t":   VarInfo("pose_t",   "pose_t",   28, "7f", True, 0), # [position, attitude]
# }

def update_var_types(data):
    """
    Adds user defined variables to the var_types dict so they can
    be used in other messages.
    """
    if "message" not in data:
        return

    name = data["message"]["name"]
    vars = data["message"]["vars"]

    if name in var_types:
        return

    msg_size = 0
    format = ''
    # print(f">> {vars}")
    for v in vars:
        if v.len > 1 and not v.complex:
            msg_size += v.size * v.len
            format += v.len * v.fmt   # str(v.len) + v.fmt
            # print(f">> {name}: {format} {v.complex}")
        else:
            msg_size += v.size
            format += v.fmt

    # VarInfo(c py size fmt complex default)
    new_var = VarInfo(name, name, msg_size, format, True, None)
    var_types[name] = new_var

class TypeBase:
    def __str__(self):
        if self.len == 1:
            return f"{self.type} {self.variable}(size={self.size}, fmt={self.fmt}, default={self.default})"
        return f"{self.type} {self.variable}[{self.len}](size={self.size}, fmt={self.fmt}, default={self.default})"

    def __repr__(self):
        return str(self)

    def c_format(self):
        """
        default: None or scalar/array
        complex: True/False
        len: 1-N

        if len > 1:
            if default:
                type var[len]{default}
        """
        default = ''
        if self.default:
            default = str(self.default)
            if default.find('[') > -1:
                default = default.replace('[','{').replace(']','}')
        if self.len > 1:
            return f"{self.type} {self.variable}[{self.len}]{default};"

        if self.complex:
            return f"{self.type} {self.variable}{default};"

        if default == '':
            return f"{self.type} {self.variable};"

        return f"{self.type} {self.variable} = {default};"

    def py_format(self):
        # if self.len == 1 and not self.complex:
        #     return f"{self.variable}: {self.type} = {self.default}"
        # # mags: list[vec_t] = field(default_factory=(lambda:[0, 0, 0]))
        # return f"{self.variable}: list[{self.type}] = field(default_factory=(lambda: {self.default}))"
        return f"{self.variable}: {self.type}"

class Scalar(TypeBase):
    def __init__(self, var, type, len):
        if not isinstance(var, str) or not isinstance(len, int) or len < 1:
            raise Exception(f"Invalid: variable: {var} and/or len: {len}")
        if not isinstance(type, str) or type not in var_types:
            raise Exception(f"Invalid: {type}")
        self.variable = var
        self.type = type
        self.len = len
        self.complex = False
        self.c = var_types[type].c
        self.py = var_types[type].py
        self.default = [0]*len if len > 1 else 0
        self.size = len*var_types[type].size
        self.fmt = f"{len}{var_types[type].fmt}" if len > 1 else var_types[type].fmt

class Quat(TypeBase):
    def __init__(self, var, len):
        if not isinstance(var, str) or not isinstance(len, int) or len < 1:
            raise Exception(f"Invalid: {var} and/or {len}")
        self.variable = var
        self.type = "quat_t"
        self.len = len
        self.complex = True
        self.default = [[1,0,0,0] for _ in range(len)] if len > 1 else [1,0,0,0]
        self.size = 4*4*len
        self.fmt = f"{4*len}f"

class Vec(TypeBase):
    def __init__(self, var, len):
        if not isinstance(var, str) or not isinstance(len, int) or len < 1:
            raise Exception(f"Invalid: {var} and/or {len}")
        self.variable = var
        self.type = "vec_t"
        self.len = len
        self.complex = True
        self.default = [[0,0,0] for _ in range(len)] if len > 1 else [0,0,0]
        self.size = 3*4*len
        self.fmt = f"{3*len}f"

class Twist(TypeBase):
    def __init__(self, var, len):
        if not isinstance(var, str) or not isinstance(len, int) or len < 1:
            raise Exception(f"Invalid: {var} and/or {len}")
        self.variable = var
        self.type = "twist_t"
        self.len = len
        self.complex = True
        self.default = [[0,0,0,0,0,0] for _ in range(len)] if len > 1 else [0,0,0,0,0,0]
        self.size = 6*4*len
        self.fmt = f"{6*len}f"

class Wrench(TypeBase):
    def __init__(self, var, len):
        if not isinstance(var, str) or not isinstance(len, int) or len < 1:
            raise Exception(f"Invalid: {var} and/or {len}")
        self.variable = var
        self.type = "wrench_t"
        self.len = len
        self.complex = True
        self.default = [[0,0,0,0,0,0] for _ in range(len)] if len > 1 else [0,0,0,0,0,0]
        self.size = 6*4*len
        self.fmt = f"{6*len}f"

class Pose(TypeBase):
    def __init__(self, var, len):
        if not isinstance(var, str) or not isinstance(len, int) or len < 1:
            raise Exception(f"Invalid: {var} and/or {len}")
        self.variable = var
        self.type = "pose_t"
        self.len = len
        self.complex = True
        self.default = [[0,0,0,1,0,0,0] for _ in range(len)] if len > 1 else [0,0,0,1,0,0,0]
        self.size = 7*4*len
        self.fmt = f"{7*len}f"

class Complex(TypeBase):
    def __init__(self, var, type, len):
        if not isinstance(var, str) or not isinstance(len, int) or len < 1:
            raise Exception(f"Invalid: variable: {var} and/or len: {len}")
        if not isinstance(type, str) or type not in var_types:
            raise Exception(f"Invalid: {type}")
        self.variable = var
        self.type = type
        self.len = len
        self.complex = True
        self.c = type
        self.py = type
        self.default = None
        self.size = len*var_types[type].size
        self.fmt = f"{len*var_types[type].fmt}" if len > 1 else var_types[type].fmt
