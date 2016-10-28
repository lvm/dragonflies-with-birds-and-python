#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import random
from utils import (
    color, image, video, helpers
)
import os
import sys
import argparse
import tempfile

import time
import datetime as dt


__file = os.path.basename(__file__)
TEMP_DIR = tempfile.mkdtemp("-arnold")
CACHE_DIR = os.path.join(TEMP_DIR, "cache")
FV_DIR = os.path.join(CACHE_DIR, "from")
TV_DIR = os.path.join(CACHE_DIR, "to")
IMG_FORMAT = "img%09d.jpg"
IMG_GLOB = "img*.jpg"


def msg(msg, verbose=False):
    if verbose:
        print ( msg )


def arnoldise(input_video, output_video):
    video_length = int(float(video.length(input_video)))

    filelist = []
    for x in range(video_length):
        t = x if x > 9 else "0{}".format(x)

        video.cut("00:00:{}".format(t), "00:00:05",
                  input_video, "cut_{}_{}".format(x,output_video))

        filelist += ["cut_{}_{}".format(x,output_video)] * random.randrange(2,10)

    helpers.write_file("list_{}.txt".format(output_video),
               map(lambda f: "file '{}'".format(f), filelist))
    video.concat("list_{}.txt".format(output_video), output_video)
    helpers.clean(filelist + ["list_{}.txt".format(output_video)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-video',
                        type=str,
                        help="Use this video as source")
    parser.add_argument('-o', '--output-video',
                        type=str,
                        required=False,
                        help="Use this video as source. Default: output.mp4")

    args = parser.parse_args()

    if args.input_video:
        arnoldise(args.input_video,
                  args.output_video or "output.mp4")
    else:
        print("{} -h".format(__file))
