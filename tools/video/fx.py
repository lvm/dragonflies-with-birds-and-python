#!/usr/bin/env python

from utils import ffmpeg

__VARS = vars()
__SIMPLE = '-vf'
__COMPLEX = '-acodec libvo_aacenc -vcodec libx264 -filter_complex'


def from_string(fx):
    v = None
    if ":" in fx:
        fx, v = fx.split(":")

    if fx and \
       fx in filter(lambda v: not v.startswith("__"), __VARS.keys()):
        fx = __VARS.get(fx)
        if callable(fx):
            return fx(v)
        else:
            return fx


def apply(fx, video_in, video_out, is_complex=False, verbose=False):
    """Applies a given `fx` to a video"""
    if isinstance(video_in, (list, tuple)):
        video_in = " ".join(map(lambda v: '-i {}'.format(v), video_in))
    else:
        video_in = '-i {}'.format(video_in)

    if isinstance(fx, (list, tuple)):
        fx = ",".join(fx) if len(fx) > 1 else str(fx[0])

    args = '{} {} "{}" {}'.format(video_in,
                                  __COMPLEX if is_complex else __SIMPLE,
                                  fx, video_out)
    ffmpeg(args, verbose)



###
# complex filters
#

# "Complex filter to blend N videos into one"
blend = "[0:v]setpts=PTS-STARTPTS, scale=480x360[top];"
blend += "[1:v]setpts=PTS-STARTPTS, scale=480x360,"
blend += "format=yuva420p,colorchannelmixer=aa=0.5[bottom];"
blend += "[top][bottom]overlay=shortest=0"


###
# selection
#

# select='lt((mod(n\,100)\,10)'

# enable=not(mod(n\,16))

def enable(frames=8):
    "Enables a filter every N frames"
    return "enable=not(mod(n\,{}))".format(frames or 8)

##
# simple filters
#
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
negative = "lutrgb='r=negval:g=negval:b=negval'"

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

# interleave 
interleave = "select='if(gt(random(0), 0.2), 1, 4)':n=2 [tmp], negate, [tmp] interleave"

##
# simple filters
#
# w/ args
#

def blur(value=5):
    "Applies a `mirror effect` to a video"
    return "boxblur={}:1".format(value or 5)


def magnify(value=2):
    "Magnifies a video"
    return "hqx={}".format(value or 2)


def random(frames=8):
    "Randomises frames of a video"
    return "random={}:-1".format(frames or 8)

def overlay(frames=8):
    "Zoom videos"
    return "select=n=2:e='not(mod(n\, {}))'+1 [odd][even]; [odd] pad=h=2/ih [tmp]; [tmp][even] overlay=y=h".format(frames or 8)


def tblend(mode='lighten'):
    "Blends frames"
    return "tblend=all_mode={}".format(mode or 'lighten')


def faster(speed=2):
    "Speeds up the video"
    return "setpts={}*PTS".format(1/(speed or 2))


def slower(speed=2):
    "Slows down the video"
    return "setpts={}*PTS".format(speed or 2)
