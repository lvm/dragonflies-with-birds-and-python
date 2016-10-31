#!/usr/bin/env python

import os

def write_file(filename, content):
    f = open(filename, 'w')
    f.write("\n".join(content))
    f.close()


def pc(n, total):
    return float(n)*(100.0/total)


def clean(filelist):
    for filename in filelist:
        try:
            os.remove(filename)
        except OSError:
            pass
