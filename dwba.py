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


def lehmannise(input_video, output_video, verbose):
    msg(">> making cache dirs", verbose)
    image.make_cache([CACHE_DIR, FV_DIR, TV_DIR])

    msg(">> video to imgs", verbose)
    video.to_images(input_video,
                    os.path.join(FV_DIR, IMG_FORMAT))

    msg(">> get color from imgs", verbose)
    imgs_data = image.avg_color_data(os.path.join(FV_DIR, IMG_GLOB))

    msg(">> build set of imgs", verbose)
    imgs_list = image.build_set(*imgs_data)

    msg(">> copy set of imgs", verbose)
    image.copy(imgs_list, TV_DIR, IMG_FORMAT)

    msg(">> imgs to video", verbose)
    video.from_images(os.path.join(TV_DIR, IMG_FORMAT), output_video)

    msg(">> cleaning cache dirs", verbose)
    image.clean_cache([FV_DIR, TV_DIR, CACHE_DIR, TEMP_DIR])


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
