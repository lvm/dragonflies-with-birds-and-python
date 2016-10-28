#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from utils import (
    color, image, video, helpers
)
from lehmann import lehmannise
from arnold import arnoldise

import os
import sys
import argparse

__file = os.path.basename(__file__)
videos = {
    'rg':{
        'list': 'rg_list',
        'video_out': 'rg.mp4',
        'a':{
            'video_in':"./videos/0781.mp4",
            'video_out':"./red.mp4",
            'start':"00:03:00",
            'duration':"00:00:10"
        },
        'b':{
            'video_in':"./videos/0781.mp4",
            'video_out':"./green.mp4",
            'start':"00:04:30",
            'duration':"00:00:10"
        }
    },

    'fin':{
        'list': 'fin_list',
        'video_out': 'fin.mp4',
        'a':{
            'video_in':"./videos/0781.mp4",
            'video_out':"./fin_a.mp4",
            'start':"00:03:10",
            'duration':"00:00:10"
        },
        'b':{
            'video_in':"./videos/0781.mp4",
            'video_out':"./fin_b.mp4",
            'start':"00:07:10",
            'duration':"00:00:10"
        }
    },

    'mex':{
        'list': 'mex_list',
        'video_out': 'mex.mp4',
        'a':{
            'video_in':"./videos/mexico.mp4",
            'video_out':"./mex_a.mp4",
            'start':"00:20:55",
            'duration':"00:00:07"
        },
        'b':{
            'video_in':"./videos/mexico.mp4",
            'video_out':"./mex_b.mp4",
            'start':"00:02:45",
            'duration':"00:00:10"
        }
    },
    'car':{
        'filelist': './car_list',
        'video_out': './car.mp4',
        'a':{
            'video_in':"./videos/mexico.mp4",
            'video_out':"./car_a.mp4",
            'start':"00:16:30",
            'duration':"00:00:10"
        },
        'b':{
            'video_in':"./videos/mexico.mp4",
            'video_out':"./car_b.mp4",
            'start':"00:42:05",
            'duration':"00:00:20"
        }
    },
    'rac':{
        'filelist': './rac_list',
        'video_out': './rac.mp4',
        'a':{
            'video_in':"./videos/mexico.mp4",
            'video_out':"./rac_a.mp4",
            'start':"00:16:30",
            'duration':"00:00:10"
        },
        'b':{
            'video_in':"./videos/mexico.mp4",
            'video_out':"./rac_b.mp4",
            'start':"00:00:51",
            'duration':"00:00:10"
        }
    },
    'trees':{
        'filelist': './trees_list',
        'video_out': './trees.mp4',
        'a':{
            'video_in':"./videos/mexico.mp4",
            'video_out':"./trees_a.mp4",
            'start':"00:23:36",
            'duration':"00:00:10"
        },
        'b':{
            'video_in':"./videos/mexico.mp4",
            'video_out':"./trees_b.mp4",
            'start':"00:53:41",
            'duration':"00:00:10"
        }
    },
    'early':{
        'filelist': './early_list',
        'video_out': './early.mp4',
        'a':{
            'video_in':"./videos/Ketcham_Home_Movies_1936_Early_Days.mp4",
            'video_out':"./early_a.mp4",
            'start':"00:00:25",
            'duration':"00:00:10"
        },
        'b':{
            'video_in':"./videos/Ketcham_Home_Movies_1936_Early_Days.mp4",
            'video_out':"./early_b.mp4",
            'start':"00:01:30.500",
            'duration':"00:00:10"
        }
    },
}


def sanitise(name):
    ext = name[-4:]
    return name.replace(ext, "").replace("/","_").replace(".","_") + ext


def build_videos(videos, name):
    v = videos.get(name)
    cuts = filter(lambda k: k not in ['filelist', 'video_out'], v.keys())

    filelist = []
    for cut in cuts:
        vc = v.get(cut)
        if type(vc) != str:
            video.cut(vc.get('start'), vc.get('duration'),
                      vc.get('video_in'), vc.get('video_out'))
            filelist += [vc.get('video_out')]

    helpers.write_file(v.get('filelist'),
                       map(lambda f: "file '{}'".format(f), filelist))
    video.concat(v.get('filelist'), v.get('video_out'), False)
    lehmannise(v.get('video_out'), "lehmann_{}".format(sanitise(v.get('video_out'))))
    arnoldise("lehmann_{}".format(sanitise(v.get('video_out'))),
              "render_{}".format(sanitise(v.get('video_out'))))

    ##
    # TODO: FIX VIDEO NAME BC THIS IS BANANAS.
    ##
    helpers.clean(filelist +[
        v.get('filelist'),
        "lehmann_{}".format(sanitise(v.get('video_out'))),
        v.get('video_out')
    ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list',
                        action="store_true",
                        help="List video-sets.")
    parser.add_argument('-v', '--video',
                        type=str,
                        required=False,
                        help="Use video-set")

    args = parser.parse_args()

    if args.list:
        print(videos.keys())
    elif args.video:
        build_videos(videos, args.video)
    else:
        print("{} -h".format(__file))
