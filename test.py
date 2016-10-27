#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import (
    color, image, video, helpers
)


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
            'video_in':"./videos/Ketcham_Home_Movies_1949_Mexico.ogv",
            'video_out':"./mex_a.ogv",
            'start':"00:20:55",
            'duration':"00:00:07"
        },
        'b':{
            'video_in':"./videos/Ketcham_Home_Movies_1949_Mexico.ogv",
            'video_out':"./mex_b.ogv",
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
            'start':"00:02:45",
            'duration':"00:00:10"
        },
        'b':{
            'video_in':"./videos/mexico.mp4",
            'video_out':"./car_b.mp4",
            'start':"00:42:05",
            'duration':"00:00:20"
        }
    },
}



def build_videos(videos, name):
    v = videos.get(name)
    cuts = filter(lambda k: k not in ['filelist', 'video_out'], v.keys())

    filelist = []
    for cut in cuts:
        vc = v.get(cut)
        video.cut(vc.get('start'), vc.get('duration'), vc.get('video_in'), vc.get('video_out'))
        filelist += ["file '{}'".format(vc.get('video_out'))]

    helpers.write_file(v.get('filelist'), filelist)
    video.concat(v.get('filelist'), v.get('video_out'), False)

build_videos(videos, 'car')
