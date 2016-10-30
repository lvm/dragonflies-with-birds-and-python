#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shlex
import argparse
import subprocess as sp

__file = os.path.basename(__file__)

def assign(fx, video_in, video_out, silent=True):
    if type(video_in) in [list, tuple]:
        video_in = " ".join(map(lambda v: '-i {}'.format(v), video_in))
    else:
        video_in = '-i {}'.format(video_in)

    """Applies a given `fx` to a video"""
    cmd = 'ffmpeg {} {} -vf "{}" {}'.format(
        '-v quiet' if silent else '',
        video_in, fx, video_out)

    sp.call(shlex.split(cmd))


def mirror(video_in, video_out, silent=True):
    """Applies a `mirror effect` to a video"""
    assign("crop=iw/2:ih:0:0,split[left][tmp];[tmp]hflip[right];[left][right] hstack",
           video_in, video_out, silent)


def blur(value, video_in, video_out, silent=True):
    """Applies a `mirror effect` to a video"""
    assign("boxblur={}:1".format(value),
           video_in, video_out, silent)


def greyscale(video_in, video_out, silent=True):
    """Converts a video to b/w"""
    assign("colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3",
           video_in, video_out, silent)


def sepia(video_in, video_out, silent=True):
    """Converts a video to `sepia`"""
    assign("colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131",
           video_in, video_out, silent)


def vintage(video_in, video_out, silent=True):
    """Gives a `vintage` look to a video"""
    assign("curves=vintage",
           video_in, video_out, silent)


def wires(video_in, video_out, silent=True):
    """Gives a `wires` look to a video"""
    assign("edgedetect=low=0.1:high=0.4",
           video_in, video_out, silent)


def paint(video_in, video_out, silent=True):
    """Gives a `paint` look to a video"""
    assign("edgedetect=mode=colormix:high=0",
           video_in, video_out, silent)


def negate(video_in, video_out, silent=True):
    """Inverts the colors in a video"""
    assign("lutrgb='r=negval:g=negval:b=negval'",
           video_in, video_out, silent)


def flip(video_in, video_out, silent=True):
    """Flips horizontally a video"""
    assign("hflip",
           video_in, video_out, silent)


def vflip(video_in, video_out, silent=True):
    """Flips vertically a video"""
    assign("vflip",
           video_in, video_out, silent)


def magnify(value, video_in, video_out, silent=True):
    """Magnifies a video"""
    assign("hqx={}".format(value),
           video_in, video_out, silent)


def kern(video_in, video_out, silent=True):
    """kernel deinterling"""
    assign("kerndeint=map=1",
           video_in, video_out, silent)


def burning(video_in, video_out, silent=True):
    """Burning effect"""
    assign("lutyuv='y=2*val'",
           video_in, video_out, silent)


def negalum(video_in, video_out, silent=True):
    """Negate Luminance effect"""
    assign("lutyuv=y=negval",
           video_in, video_out, silent)


def noise(video_in, video_out, silent=True):
    """Noise effect"""
    assign("noise=alls=20:allf=t+u",
           video_in, video_out, silent)


def to_palette(video_in, image_out, silent=True):
    """Saves a palette from a video"""
    assign("palettegen",
           video_in, image_out, silent)


def from_palette(palette_in, video_in, video_out, silent=True):
    """Saves a palette from a video"""
    assign("palettegen",
           [palette_in, video_in], video_out, silent)


def random(frames, video_in, video_out, silent=True):
    """Randomises frames of a video"""
    assign("random={}:-1".format(frames),
           video_in, video_out, silent)


def reverse(video_in, video_out, silent=True):
    """Randomises frames of a video"""
    assign("reverse",
           video_in, video_out, silent)


def shuffleframes(video_in, video_out, silent=True):
    """Shuffles frames of a video"""
    #assign("shuffleframes=...",
    #       video_in, video_out, silent)


def portrait(video_in, video_out, silent=True):
    """Portrait"""
    assign("transpose=1:portrait",
           video_in, video_out, silent)


def vignette(video_in, video_out, silent=True):
    """Vignettes a video"""
    assign("vignette='PI/4+random(1)*PI/50':eval=frame",
           video_in, video_out, silent)


def zoom(video_in, video_out, silent=True):
    """Zoom videos"""
    assign("zoompan=z='min(max(zoom,pzoom)+0.0015,1.5)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
           video_in, video_out, silent)


def overlay(video_in, video_out, silent=True):
    """Zoom videos"""
    assign("select=n=2:e='not(mod(n\, 4))'+1 [odd][even]; [odd] pad=h=2/ih [tmp]; [tmp][even] overlay=y=h",
           video_in, video_out, silent)


def blend(mode, video_in, video_out, silent=True):
    """Blends frames"""
    assign("tblend=all_mode={}".format(mode),
           video_in, video_out, silent)
