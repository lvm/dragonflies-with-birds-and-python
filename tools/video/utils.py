#!/usr/bin/env python

import os
import shlex
import argparse
import tempfile
import subprocess as sp
from ..helpers import write_file
from ..fs import rm_files


def ffmpeg(args, verbose=False):
    "Base ffmpeg system call"
    cmd = "ffmpeg {} -y {}".format(
        '' if verbose else '-v quiet',
        args
    )
    sp.call(shlex.split(cmd))


def ffprobe(args, verbose=False):
    "Base ffprobe system call"
    cmd = "ffprobe {} {}".format(
        '' if verbose else '-v quiet',
        args
    )
    return sp.check_output(shlex.split(cmd))


###
# conversions
#

def to_images(video_in, img_format, verbose=False):
    "Converts a video to an image sequence"
    args = "-i {} -q:v 2 {}".format(video_in, img_format)
    ffmpeg(args, verbose)


def to_frames(video_in, img_format, fps=12, verbose=False):
    "Converts a video to an image sequence every N frames (default: 12)"
    args = '-i {} -vf "select=not(mod(n\,{}))" '.format(video_in, fps)
    args += '-vsync vfr -q:v 2 {}'.format(img_format)
    ffmpeg(args, verbose)


def to_video(video_out, img_format, fps=12, verbose=False):
    "Converts an image sequence to a video"
    args = '-y -i {} -c:v libx264 -vf fps={} -pix_fmt yuv420p {}'.format(
        img_format, fps, video_out)
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
    args = '-show_format {} -i {}'.format(
        '-sexagesimal' if show_sexagesimal else '',
        video_in)
    output = ffprobe(args, verbose)
    return map(lambda line: line.replace(duration, ''),
               filter(lambda line: line.startswith(duration),
                      output.split("\n")))[0]


def cut(video_in, video_out, start, duration, verbose=False):
    "Cuts a portion of a video."
    if isinstance(video_in, (list, tuple)):
        video_in = video_in[0]

    args = '-i {} -ss "{}" -t "{}" -c copy -an {}'.format(
        video_in, start, duration, video_out)
    ffmpeg(args, verbose)


def cut_reencode(video_in, video_out, start, duration, verbose=False):
    "Cuts a portion and re-encodes a video"
    if isinstance(video_in, (list, tuple)):
        video_in = video_in[0]

    args = '-i {} -ss "{}" -t "{}" -c:v libx264 -c:a aac -strict experimental -b:a 128k {}'.format(
        video_in, start, duration, video_out)
    ffmpeg(args, verbose)


def glue(videos_in, video_out, verbose=False):
    "Glues a list of videos in a single one"
    if not isinstance(videos_in, (list, tuple)):
        # must be a list or a tuple, silly.
        return

    tmpfile = tempfile.mktemp()
    content = map(lambda v: "file '{}'".format(os.path.abspath(v)), videos_in)
    args = "-f concat -safe 0 -i {} -c copy {}".format(tmpfile, video_out)
    write_file(tmpfile, content)
    ffmpeg(args, verbose)
    rm_files(tmpfile)


def convert_framerate(video_in, video_out, fps=12, verbose=False):
    "Converts the framerate of a video"
    args = "-i {} -qscale 0 -r {} -y {}".format(
        video_in, fps, video_out)
    ffmpeg(args, verbose)
