#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 20.02.2024
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com

import argparse
from .decompose import run_it as decompose
from .rotate import run_it as rotate

def main():
    parser = argparse.ArgumentParser(description="Toolset for decomposing repeats into monomers.")
    parser.add_argument('command', help="The command to execute (run, rotate) [run]", default="run")
    parser.add_argument('args', nargs=argparse.REMAINDER, help="Arguments to pass to the command.")

    args = parser.parse_args()

    if args.command == 'run':
        decompose(args.args)
    elif args.command == 'rotate':
        rotate(args.args)
    else:
        print("Unknown command:", args.command)

if __name__ == "__main__":
    main()