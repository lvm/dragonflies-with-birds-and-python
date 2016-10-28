#!/usr/bin/env python

import os
import re
import argparse
import tempfile
import operator as op


__file = os.path.basename(__file__)
TEMP_DIR = tempfile.mkdtemp("-lang")
CACHE_DIR = os.path.join(TEMP_DIR, "cache")


PARSECODE_RE = "(?P<action>\w+)\s?{(?P<codeblock>.[^}]*)}"
PARSECODE = re.compile(PARSECODE_RE, re.DOTALL)

PARSEBLOCK_RE = "(?P<fn>\w+)\s\"(?P<param>.[^\"]*)\""
PARSEBLOCK = re.compile(PARSEBLOCK_RE, re.DOTALL)


def read(filename, verbose):
    "Reads the code and renders a video"
    program = " ".join(open(filename, 'r').readlines())

    for action, codeblock in PARSECODE.findall(program):
        print action
        for fn, param in PARSEBLOCK.findall(codeblock):
            print fn
            print param
            print
        print "-"*80


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename',
                        type=str,
                        help="Use this source code")
    parser.add_argument('-V', '--verbose',
                        action="store_true",
                        help="Show stdout messages")

    args = parser.parse_args()
    if args.filename:
        read(args.filename,
             args.verbose or False)
    else:
        print("{} -h".format(__file))
