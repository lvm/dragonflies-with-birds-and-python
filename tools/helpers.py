#!/usr/bin/env python

import os


def write_file(filename, content):
    "Receives an array of (unicode) strings and writes them to a file"
    f = open(filename, 'w')
    f.write("\n".join(map(unicode, content)))
    f.close()


def pc(n, total):
    "Calculates percentage"
    return float(n)*(100.0/total)
