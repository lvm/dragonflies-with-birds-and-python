#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shlex
import argparse
import subprocess as sp
import fx

__file = os.path.basename(__file__)


###
# conversions
#

def to_images(video, images_format):
    """Converts a video to an image sequence.
    Use in conjunction with `--video` and `--image`
    {} --to-images --video video.mp4 --image img*.jpg
    """.format(__file)
    sp.call(['ffmpeg',
             '-v', 'quiet',
             '-y', '-i', video,
             '-q:v', '2', images_format
    ])


def to_frames(video, images_format, fps=12):
    """Converts a video to an image sequence every N frames (default: 12).
    Use in conjunction with `--video` and `--image`
    {} --to-images --video video.mp4 --image img*.jpg
    """.format(__file)
    cmd = 'ffmpeg -v quiet -y -i {} -vf "select=not(mod(n\,{}))"'.format(video, fps)
    cmd+= ' -vsync vfr -q:v 2 ' + images_format

    sp.call(shlex.split(cmd))


def to_video(images_format, video, fps=12):
    """Converts an image sequence to a video.
    Use in conjunction with `--video` and `--image`
    {} --to-video --image img*.jpg --video video.mp4
    """.format(__file)

    sp.call(['ffmpeg',
             '-v', 'quiet',
             #'-framerate', str(fps),
             '-i', images_format,
             '-c:v', 'libx264',
             '-vf', 'fps={}'.format(fps),
             '-pix_fmt', 'yuv420p',
             video
    ])


###
# operations
#

def length(video_in, show_sexagesimal=False):
    """Converts the framerate of a video.
    Use in conjunction with `--video` and `--fps`.
    {} --convert-framerate --video video.mp4 --fps 12
    """.format(__file)

    cmd = 'ffprobe -v quiet -show_format {} -i {}'.format(
        '-sexagesimal' if show_sexagesimal else '',
        video_in)

    duration = 'duration='
    output = sp.check_output(shlex.split(cmd))
    return map(lambda line: line.replace(duration, ''),
               filter(lambda line: line.startswith(duration),
                      output.split("\n")))[0]


def cut(start, duration, video_in, video_out):
    """Cuts a portion of a video.
    Use in conjunction with `--video`, `--start`, `--duration` and (optional)`--video-out`.
    Doesn't re-encode the video by default, except with the `--reencode` flag.
    {} --video-cut --video video.mp4 --start 00:02:30 --duration 00:00:30
    """.format(__file)

    sp.call(['ffmpeg',
           '-v', 'quiet',
           '-i', str(video_in),
           '-ss', '{}'.format(start),
           '-t', '{}'.format(duration),
           '-c', 'copy',
           video_out or "cut_output.mp4"
    ])


def cut_reencode(start, duration, video_in, video_out):
    """Cuts a portion of a video.
    Use in conjunction with `--video`, `--start`, `--duration` and (optional)`--re-encode`.
    {} --video-cut --video video.mp4 --start 00:02:30 --duration 00:00:30
    """.format(__file)

    sp.call(['ffmpeg',
             '-v', 'quiet',
             '-ss', start,
             '-i', video_in,
             '-t', duration,
             '-c:v', 'libx264',
             '-c:a', 'aac',
             '-strict', 'experimental',
             '-b', '128k',
             video_out or "cut_output.mp4"
    ])


def concat(filelist, video_out, silent=True):
    """Concatenages a list of videos take from
    a file list
    {} --concatenate --file list.txt
    """.format(__file)

    cmd = "ffmpeg {} -f concat -safe 0 -i {} -c copy {}".format(
        '-v quiet' if silent else '',
        filelist, video_out)
    sp.call(shlex.split(cmd))


def convert_framerate(fps, video_in, video_out):
    """Converts the framerate of a video.
    Use in conjunction with `--video` and `--fps`.
    {} --convert-framerate --video video.mp4 --fps 12
    """.format(__file)

    sp.call(['ffmpeg',
             '-v', 'quiet',
             '-i', video_in,
             '-qscale', '0',
             '-r', fps,
             '-y',
             video_out or "cut_output.mp4"
    ])
