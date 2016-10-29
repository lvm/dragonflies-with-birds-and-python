#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shlex
import argparse
import subprocess as sp

__file = os.path.basename(__file__)


def missing_parameters(help_msg):
    print "{}\n{}".format("Missing Parameters!", help_msg)


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


###
# effects
#


def effect(fx, video_in, video_out, silent=True):

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
    effect("crop=iw/2:ih:0:0,split[left][tmp];[tmp]hflip[right];[left][right] hstack",
           video_in, video_out, silent)


def blur(value, video_in, video_out, silent=True):
    """Applies a `mirror effect` to a video"""
    effect("boxblur={}:1".format(value),
           video_in, video_out, silent)


def greyscale(video_in, video_out, silent=True):
    """Converts a video to b/w"""
    effect("colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3",
           video_in, video_out, silent)


def sepia(video_in, video_out, silent=True):
    """Converts a video to `sepia`"""
    effect("colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131",
           video_in, video_out, silent)


def vintage(video_in, video_out, silent=True):
    """Gives a `vintage` look to a video"""
    effect("curves=vintage",
           video_in, video_out, silent)


def wires(video_in, video_out, silent=True):
    """Gives a `wires` look to a video"""
    effect("edgedetect=low=0.1:high=0.4",
           video_in, video_out, silent)


def paint(video_in, video_out, silent=True):
    """Gives a `paint` look to a video"""
    effect("edgedetect=mode=colormix:high=0",
           video_in, video_out, silent)


def negate(video_in, video_out, silent=True):
    """Inverts the colors in a video"""
    effect("lutrgb='r=negval:g=negval:b=negval'",
           video_in, video_out, silent)


def flip(video_in, video_out, silent=True):
    """Flips horizontally a video"""
    effect("hflip",
           video_in, video_out, silent)


def vflip(video_in, video_out, silent=True):
    """Flips vertically a video"""
    effect("vflip",
           video_in, video_out, silent)


def magnify(value, video_in, video_out, silent=True):
    """Magnifies a video"""
    effect("hqx={}".format(value),
           video_in, video_out, silent)


def kern(video_in, video_out, silent=True):
    """kernel deinterling"""
    effect("kerndeint=map=1",
           video_in, video_out, silent)


def burning(video_in, video_out, silent=True):
    """Burning effect"""
    effect("lutyuv='y=2*val'",
           video_in, video_out, silent)


def negalum(video_in, video_out, silent=True):
    """Negate Luminance effect"""
    effect("lutyuv=y=negval",
           video_in, video_out, silent)


def noise(video_in, video_out, silent=True):
    """Noise effect"""
    effect("noise=alls=20:allf=t+u",
           video_in, video_out, silent)


def to_palette(video_in, image_out, silent=True):
    """Saves a palette from a video"""
    effect("palettegen",
           video_in, image_out, silent)


def from_palette(palette_in, video_in, video_out, silent=True):
    """Saves a palette from a video"""
    effect("palettegen",
           [palette_in, video_in], video_out, silent)


def random(frames, video_in, video_out, silent=True):
    """Randomises frames of a video"""
    effect("random={}:-1".format(frames),
           video_in, video_out, silent)


def reverse(video_in, video_out, silent=True):
    """Randomises frames of a video"""
    effect("reverse",
           video_in, video_out, silent)


def shuffleframes(video_in, video_out, silent=True):
    """Shuffles frames of a video"""
    #effect("shuffleframes=...",
    #       video_in, video_out, silent)


def transpose(video_in, video_out, silent=True):
    """Shuffles frames of a video"""
    effect("transpose=1:portrait",
           video_in, video_out, silent)


def vignette(video_in, video_out, silent=True):
    """Shuffles frames of a video"""
    effect("vignette='PI/4+random(1)*PI/50':eval=frame",
           video_in, video_out, silent)


    


if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('-ti', '--to-images',
                            action="store_true",
                            help=to_images.__doc__)
        parser.add_argument('-tv', '--to-video',
                            action="store_true",
                            help=to_video.__doc__)
        parser.add_argument('-vc', '--video-cut',
                            action="store_true",
                            help=cut_video.__doc__)
        parser.add_argument('-cf', '--convert-framerate',
                            action="store_true",
                            help=convert_framerate.__doc__)


        parser.add_argument('-r', '--re-encode',
                            action="store_true",
                            help="""Re-encodes a video.""".format(__file))
        parser.add_argument('-i', '--images',
                            type=str,
                            required=False,
                            help="An image sequence to work with. eg: img*.jpg.")
        parser.add_argument('-v', '--video',
                            type=str,
                            required=False,
                            help="A video to work with. eg: video.mp4.")
        parser.add_argument('-s', '--start',
                            type=str,
                            required=False,
                            help="A video position. eg: hh:mm:ss.")
        parser.add_argument('-d', '--duration',
                            type=str,
                            required=False,
                            help="A time frame. eg: hh:mm:ss.")
        parser.add_argument('-fps', '--framerate',
                            type=str,
                            required=False,
                            help="A framerate. eg: 12 or 24 or 25 or 30.")

        args = parser.parse_args()

        if args.to_images:
            if args.video and args.images:
                to_images(args.video, args.images)
            else:
                missing_parameters(to_images.__doc__)
        elif args.to_video:
            if args.video and args.images:
                to_video(args.images, args.video)
            else:
                missing_parameters(to_video.__doc__)
        elif args.video_cut:
            if args.start and args.duration and args.video:
                if args.re_encode:
                    cut_video_reencode(args.video, args.start, args.duration)
                else:
                    cut_video(args.video, args.start, args.duration)
            else:
                missing_parameters(cut_video.__doc__)
        elif args.convert_framerate:
            if args.video and args.framerate:
                convert_framerate(args.video, args.framerate)
            else:
                missing_parameters(convert_framerate.__doc__)
        else:
            print "{} -h".format(__file)

            
