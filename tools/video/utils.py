#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shlex
import argparse
import tempfile
import subprocess as sp
from ..helpers import (
    write_file, clean
)


def ffmpeg(args, verbose=False, check_output=False):
    "Base ffmpeg system call"
    cmd = "ffmpeg {} {}".format(
        '' if verbose else '-v quiet',
        args
    )
    if check_output:
        sp.check_output(shlex.split(cmd))
    else:
        sp.call(shlex.split(cmd))


###
# conversions
#

def to_images(video_in, img_format, verbose=False):
    "Converts a video to an image sequence"
    args = "y -i {} -q:v 2 {}".format(video_in, img_format)
    ffmpeg(args, verbose)


def to_frames(video_in, img_format, fps=12, verbose=False):
    "Converts a video to an image sequence every N frames (default: 12)"
    args = '-y -i {} -vf "select=not(mod(n\,{}))" '.format(video_in, fps)
    args += '-vsync vfr -q:v 2 {}'.format(img_format)
    ffmpeg(args, verbose)


def to_video(video_out, img_format, fps=12, verbose=False):
    "Converts an image sequence to a video"
    cmd = '-i {} -c:v libx264 -vf fps={} -pix_fmt yuv420p {}'.format(
        images_format,fps, video_out)
    ffmpeg(args, verbose)


def to_palette(video_in, image_out, silent=True):
    "Saves a palette from a video"
    return "palettegen"


def from_palette(palette_in=''):
    "Saves a palette from a video"
    return "palettegen"


###
# operations
#

def length(video_in, show_sexagesimal=False, verbose=False):
    "Returns the length of a video"
    duration = 'duration='
    args = 'ffprobe -v quiet -show_format {} -i {}'.format(
        '-sexagesimal' if show_sexagesimal else '',
        video_in)
    output = ffmpeg(args, verbose)

    return map(lambda line: line.replace(duration, ''),
               filter(lambda line: line.startswith(duration),
                      output.split("\n")))[0]


def cut(video_in, video_out, start, duration, verbose=False):
    "Cuts a portion of a video."
    args = '-i {} -ss "{}" -t "{}" -c copy {}'.format(
        video_in, start, duration, video_out)
    ffmpeg(args, verbose)


def cut_reencode(video_in, video_out, start, duration, verbose=False):
    "Cuts a portion and re-encodes a video"
    args = '-i {} -ss "{}" -t "{}" -c:v libx264 -c:a aac -strict experimental -b 128k {}'.format(
        video_in, start, duration, video_out)
    ffmpeg(args, verbose)


def glue(videos_in, video_out, verbose=False):
    "Glues a list of videos in a single one"
    if type(videos_in) not in [list, tuple]:
        return # must be a list or a tuple, silly.
    tmpfile = tempfile.mktemp()
    content = map(lambda v: "file '{}'".format(os.path.abspath(v)), videos_in)
    args = "-f concat -safe 0 -i {} -c copy {}".format(tmpfile, video_out)
    write_file(tmpfile, content)
    ffmpeg(args, verbose)
    clean(tmpfile)


def convert_framerate(video_in, video_out, fps=12, verbose=False):
    "Converts the framerate of a video"
    args = '-i {} -qscale 0 -r {} -y {}'.format(
        video_in, fps, video_out)
    ffmpeg(args, verbose)
