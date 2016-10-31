#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from __future__ import print_function

import random
from utils import (
    color, image, video, helpers
)
import os
import sys
import argparse

import time
import datetime as dt

from lehmann import lehmannise
from arnold import arnoldise

from textx.metamodel import metamodel_from_file


TV = metamodel_from_file('utils/grammar.tx', ignore_case=True)


class Video(object):
    def __init__(self, name):
        self.name = name
        self.tmpfile = "{}-{}".format(tempfile, name)


    def cut(self, video_in, video_out, start, duration, verbose):
        video.cut(video_in, video_out, start, duration, verbose)


    def glue(self, video_in, video_out):
        video.cut(video_in, video_out, start, duration, verbose)
        pass


    def apply(self):
        pass


    def action(self, action, codeblock, verbose):
        if action == "cut":
            pass

        if action == "glue":
            pass

        if action == "apply":
            pass



def read(filename, verbose):
    if os.path.isfile(filename):
        _model = TV.model_from_file(filename)
        v_name = os.path.basename(os.path.splitext(filename))[0]
        video = Video(v_name)

        for act in _model.actions:
            video.action(act.action,
                         dict(using=act.using,
                              render=act.render,
                              start=act.start,
                              duration=act.duration,
                              fx=act.fx),
                         verbose)


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
