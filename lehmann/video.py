#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess as sp


def to_images(video, images_format):
    "Converts a video to a series of images using `ffmpeg`"
    if os.path.isfile(video):
        sp.call(['ffmpeg', '-y', '-i', video,
                 '-qscale', '0', images_format])


def from_images(images_format, video):
    "Converts a video from a series of images using `ffmpeg`"
    sp.call(['ffmpeg',
             '-framerate', '9',
             '-i', images_format,
             '-c:v', 'libx264',
             '-vf', 'fps=25',
             '-pix_fmt', 'yuv420p',
             video])
