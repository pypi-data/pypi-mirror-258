#!/usr/bin/env python3
#-*-coding:utf-8-*-
from colorama import Fore
from pathlib import Path
import gecko_messages as gmsgs
import argparse

DESCRIPTION = f"""
Generate cpp and python messages from toml templates.

Author:  {gmsgs.__author__}
Version: {gmsgs.__version__}
License: {gmsgs.__license__}
"""

def handleArgs():
    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i','--in_path', help='path to message tomls', type=str, default=".")
    parser.add_argument('-o','--out_path', help='path to save to', type=str, default=".")
    parser.add_argument('-co','--cpp_only', help='C++ only', action='store_true')
    parser.add_argument('-po','--python_only', help='Python only', action='store_true')

    args = vars(parser.parse_args())
    return args

def language(data, create, output_path, ext):
    print(f"{Fore.GREEN} Saving to {output_path.resolve()}{Fore.RESET}")
    for msg in data:
        name = msg["message"]["name"]
        print(f"{Fore.CYAN} -> {name}{ext}{Fore.RESET}")
        content = create(msg)
        name += ext
        gmsgs.write_file(output_path / name, content)


def main():
    args = handleArgs()
    # print(args)

    in_path = Path(args["in_path"])
    out_path = Path(args["out_path"])

    data = gmsgs.read_folder(in_path)
    gmsgs.print_summary(data)

    py, cpp = True, True
    if args["cpp_only"]:
        py = False
        cpp = True
    if args["python_only"]:
        cpp = False
        py = True

    if cpp:
        print(f"{Fore.GREEN}[ C++ ]{Fore.RESET}")
        language(data, gmsgs.create_cpp, out_path / "cpp", ".hpp")

    if py:
        print(f"{Fore.GREEN}[ Python ]{Fore.RESET}")
        language(data, gmsgs.create_python, out_path / "python", ".py")

if __name__ == "__main__":
    main()