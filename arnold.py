#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from lehmann import (
    color, image, video
)
import os
import argparse
import tempfile


__file = os.path.basename(__file__)
TEMP_DIR = tempfile.mkdtemp("-dwbapy")
CACHE_DIR = os.path.join(TEMP_DIR, "cache")
FV_DIR = os.path.join(CACHE_DIR, "from")
TV_DIR = os.path.join(CACHE_DIR, "to")
IMG_FORMAT = "img%09d.jpg"
IMG_GLOB = "img*.jpg"

def msg(msg, verbose=False):
    if verbose:
        print ( msg )


def arnoldise(input_video, output_video, verbose):
    video_length = float(video.length(input_video))

    video.cut("00:00:01", "00:00:10", input_video, output_video)

    print (video_length)


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
        lehmannise(args.input_video,
                   args.output_video or "output.mp4",
                   args.verbose)
    else:
        print("{} -h".format(__file))
