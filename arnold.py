#!/usr/bin/env python

import random
from tools import (
    color, image, video, fs
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
        print(msg)


def arnoldise(input_video, output_video, verbose=False):
    video_length = int(float(video.utils.length(input_video, False, verbose)))
    filelist = []
    for x in range(video_length):
        t = x if x > 9 else "0{}".format(x)

        video.utils.cut(input_video,
                        "./cut_{}_{}".format(x, output_video),
                        "00:00:{}".format(t), "00:00:05",
                        verbose)

        if x % 4 == 0:
            video.fx.apply(
                map(video.fx.from_string, ["blend:and", "slower"]),
                "./cut_{}_{}".format(x, output_video),
                "./cut_{}_{}".format(x, output_video),
                verbose)

        filelist += ["cut_{}_{}".format(
            x, output_video)] * random.randrange(2, 10)

    video.utils.glue(filelist, output_video, verbose)
    fs.rm_files(filelist)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-video',
                        type=str,
                        help="Use this video as source")
    parser.add_argument('-o', '--output-video',
                        type=str,
                        required=False,
                        help="Use this video as source. Default: output.mp4")
    parser.add_argument('-V', '--verbose',
                        action="store_true",
                        help="Show stdout messages")

    args = parser.parse_args()

    if args.input_video:
        arnoldise(args.input_video,
                  args.output_video or "output.mp4",
                  args.verbose or False)
    else:
        print("{} -h".format(__file))
