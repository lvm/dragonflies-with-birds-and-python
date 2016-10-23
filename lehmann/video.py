#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import subprocess as sp


__file = os.path.basename(__file__)


def missing_parameters(help_msg):
    print "{}\n{}".format("Missing Parameters!", help_msg)


def to_images(video, images_format):
    """Converts a video to an image sequence.
    Use in conjunction with `--video` and `--image`
    {} --to-images --video video.mp4 --image img*.jpg
    """.format(__file)

    sp.call(['ffmpeg', '-y', '-i', video,
             '-qscale', '0', images_format
    ])


def to_video(images_format, video):
    """Converts an image sequence to a video.
    Use in conjunction with `--video` and `--image`
    {} --to-video --image img*.jpg --video video.mp4
    """.format(__file)

    sp.call(['ffmpeg',
             '-framerate', '9',
             '-i', images_format,
             '-c:v', 'libx264',
             '-vf', 'fps=25',
             '-pix_fmt', 'yuv420p',
             video
    ])


def cut_video(video_in, start, duration):
    """Cuts a portion of a video.
    Use in conjunction with `--video`, `--start`, `--duration` and (optional)`--video-out`.
    Doesn't re-encode the video by default, except with the `--reencode` flag.
    {} --video-cut --video video.mp4 --start 00:02:30 --duration 00:00:30
    """.format(__file)

    sp.call(['ffmpeg',
             '-i', video_in,
             '-ss', start,
             '-t', duration,
             '-c', 'copy',
             "cut_{}".format(video_in)
    ])


def cut_video_reencode(video_in, start, duration):
    """Cuts a portion of a video.
    Use in conjunction with `--video`, `--start`, `--duration` and (optional)`--re-encode`.
    {} --video-cut --video video.mp4 --start 00:02:30 --duration 00:00:30
    """.format(__file)

    sp.call(['ffmpeg',
             '-ss', start,
             '-i', video_in,
             '-t', duration,
             '-c:v', 'libx264',
             '-c:a', 'aac',
             '-strict', 'experimental',
             '-b', '128k',
             "cutr_{}".format(video_in)
    ])


def convert_framerate(video_in, fps):
    """Converts the framerate of a video.
    Use in conjunction with `--video` and `--fps`.
    {} --convert-framerate --video video.mp4 --fps 12
    """.format(__file)

    sp.call(['ffmpeg',
             '-i', video_in,
             '-qscale', '0',
             '-r', fps,
             '-y',
             "fps_{}".format(video_in)
    ])


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
