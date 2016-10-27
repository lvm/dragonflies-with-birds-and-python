#!/usr/bin/env python
# -*- coding: utf-8 -*-

def write_file(filename, content):
    f = open(filename, 'w')
    f.write("\n".join(content))
    f.close()


def pc(n, total):
    return float(n)*(100.0/total)
