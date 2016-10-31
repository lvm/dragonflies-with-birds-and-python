#!/usr/bin/env python

from utils import ffmpeg

def apply(fx, video_in, video_out, verbose=False):
    """Applies a given `fx` to a video"""
    if type(video_in) in [list, tuple]:
        video_in = " ".join(map(lambda v: '-i {}'.format(v), video_in))
    else:
        video_in = '-i {}'.format(video_in)

    if type(fx) in [list, tuple]:
        fx = ",".join(fx) if len(fx) > 1 else str(fx[0])

    args = '{} -vf "{}" {}'.format(video_in, fx, video_out)
    ffmpeg(args, cmd)


##
# w/o args
#

# Applies a `mirror effect` to a video
mirror = "crop=iw/2:ih:0:0,split[left][tmp];[tmp]hflip[right];[left][right] hstack"

# Converts a video to b/w
greyscale = "colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3"

# Converts a video to `sepia`
sepia = "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131"

# Gives a `vintage` look to a video
vintage = "curves=vintage"

# Gives a `wires` look to a video
wires = "edgedetect=low=0.1:high=0.4"

# Gives a `paint` look to a video
paint = "edgedetect=mode=colormix:high=0"

# Inverts the colors in a video
negate = "lutrgb='r=negval:g=negval:b=negval'"

# Flips horizontally a video
hflip = "hflip"

# Flips vertically a video
vflip = "vflip"

# kernel deinterling
kern = "kerndeint=map=1"

# Burning effect
burning = "lutyuv='y=2*val'"

# Negate Luminance effect
negalum = "lutyuv=y=negval"

# Noise effect
noise = "noise=alls=20:allf=t+u"

# reverse a video
reverse = "reverse"

# Portrait
portrait = "transpose=1:portrait"

# Vignettes a video
vignette = "vignette='PI/4+random(1)*PI/50':eval=frame"

# Zoom videos
zoom = "zoompan=z='min(max(zoom,pzoom)+0.0015,1.5)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"

##
# w/ args
#

def blur(value=5):
    "Applies a `mirror effect` to a video"
    return "boxblur={}:1".format(value)


def magnify(value=2):
    "Magnifies a video"
    return "hqx={}".format(value)


def random(frames=8):
    "Randomises frames of a video"
    return "random={}:-1".format(frames)


def overlay(frames):
    "Zoom videos"
    return "select=n=2:e='not(mod(n\, {}))'+1 [odd][even]; [odd] pad=h=2/ih [tmp]; [tmp][even] overlay=y=h".format(frames)


def blend(mode='lighten'):
    "Blends frames"
    return "tblend=all_mode={}".format(mode)

