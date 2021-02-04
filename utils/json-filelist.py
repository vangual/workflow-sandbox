#!/usr/bin/env python3
# This tool lists files in a given folder in a json array
# Author: Samuel Graenacher
import json
import argparse
import pathlib

parser = argparse.ArgumentParser(description='List files in given folder as json list')
parser.add_argument('folder', type=pathlib.Path, help='Folder to start in')
parser.add_argument('-r', '--recurse', action='store_true', help='Recurse into subdirectories')
parser.add_argument('-p', '--pattern', help='Only show files matching this pattern', default='*.*')
parser.add_argument('-f', '--folders', action='store_true', help='Include folders in output')
parser.add_argument('-a', '--absolute', action='store_true', help='All paths are output as absolute')


args = parser.parse_args()

recurse_pattern = '**/' if args.recurse else ''

try:
    pathlist = args.folder.glob(recurse_pattern + args.pattern)

    output = []

    for path in pathlist:
        if path.is_dir() and not args.folders:
            continue  # Skipping folders as option wasn't given
        if args.absolute:
            path_to_add = str(path.resolve())
        else:
            path_to_add = str(path.relative_to(args.folder))
        output.append(path_to_add)

except OSError:
    print("[]")

try:
    print(json.dumps(output))
except TypeError:
    print("[]")
