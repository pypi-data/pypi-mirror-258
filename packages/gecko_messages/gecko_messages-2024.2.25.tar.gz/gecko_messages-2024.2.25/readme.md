# Messages

Message formats should be short and simple, but if you want, it can also be complex.

Files:

- `imu.toml` where the name of the message is the name of the file
- `global.toml` which holds common or global setting for all

```
toml(file) - > dict -> create_c/py -> string -> file
toml(string) -> dict -> create_c/py -> string -> file

read_folder(dir_path, output_path=./) -> calls below functions
read_toml(file) -> dict
read_tomls(string) -> dict

Msg_file(file_path, global_file=file_path/global.toml, output_path=./) -> string
Msg_string(str, global_str) -> string
```

Binary:
https://linuxcommandlibrary.com/man/protoc

```
msgcomp [--out_dir=DIR][--in_dir=DIR][--version][--verbose][--help][--cpp-only][--python-only]
```

verbose:
num msg found: x
global found: t/f
Id, Msg_name, size, fmt
…

Cpp and python need id2msg(int) -> string

## Message File

Message use standard types:

- `uint8` or `int8`
- `uint16` or `int16`
- `uint32` or `int32`
- `uint64` or `int64`
- `float`

Or complex types:

| ID | Message    | Info                             |
|----|------------|----------------------------------|
| 1  | `vec_t`    | {float x,y,z}
| 2  | `quat_t`   | {float w,x,y,z}
| 3  | `twist_t`  | {vec_t linear, vec_t angular}
| 4  | `wrench_t` | {vec_t force, vec_t torque}
| 5  | `pose_t`   | {vec_t position, quat_t orientation}


## Global

Now you can shorten your message file because a lot of the keys are repetitive across
message files. Basically, anything in the “global” space of a message file can be moved
to a `global.toml` file instead of putting it into a message file.

```toml
[global]
comments = "string"
namespace = "string"
license = "string" # full text of what you want at the top of each file
version = "string" # anything you want like 1.0.2 or 2022.2.23
frozen = "bool"    # is python dataclass frozen true or false
wrap_width = "int" # line width for text wrapping, default = 70

[global.serialize]
yivo = "bool"         # true | false
mavlink = "bool"

# put native types in var_types VarTypes(name, size, fmt, id) ... native ids = 0,
# complex ids > 0, remove complex altogether ids between 20 - 255. This is nice
# to put message ids here, because you can see them all in one place and know you don’t
# have any conflicts.
[global.ids]
imu_t = int
calibration_t = int
my_cool_msg = int
awesome_msg = int
```

## Message

```toml
[enum.name] # optional, can have many of these, each must have
            # an original name and each value in an enum must
            # be unique (python uses `@unique` from `enum`
            # library)
Val1 = 1
Val2 = 2
Val3 = 3

# since python is not a strongly typed language, it will not always respect
# default types, so what should be an array (float[3]), you can set to a
# scalar int. C is the only one that will complain if you do this.
[message]
# type-var_name = array_dimension
float-x = 1  # float x = 0 or default
float-y = 2  # float y[2]{0,0} or default
float-z = 1  # var names can only be ascii letters, numbers and -
vec_t-a = 2  # vec_t a[2]{{0,0,0},{0,0,0}}
             # add `#include “vec_t.hpp”` and `from vec_t import *` when generated

comments = "string"     # optional, will be attached to the `struct`
id = "bool"             # can be in global.toml [ids] or here, value must be between 20 - 255
frozen = "bool"         # only for python dataclass

[message.defaults] # optional, don't need to do this
x = 12      # set defaults for variables
y = [1,2]   # don't need to define defaults for all variables

# this is really a message library for serialization, so only put functions if
# you really need to, otherwise, let some other part of your code base
# handle this
[functions]
c = "string"
python = "string"
```

The minimum message file is:

```toml
[message]
float-x = 1
id = 33  # this can be in global.toml under [global.ids]
name = "simple"
```

## To Do

- [x] Add defaults to message
- [ ] Fix `python` 3.8 - 3.10 with `tomlkit`
- [x] Added ranges to types, but don't use them, remove?
- [ ] Add global wrap size default to 70 char wide
- [ ] Add `py` and `c` for builtin messages, want `vec` in message and `vec_t` in `c`
- [ ] Fix comments ... do I need them?
- [ ] Fix or remove automatic defaults, messages with new types are not
      getting setup correctly with defaults. Only allow custom defaults
      for new messages. Maybe embed default in each type class or `None`
      if no default?

# MIT License

**Copyright (c) 2023 gecko-robotics**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.