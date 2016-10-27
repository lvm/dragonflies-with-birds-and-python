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
    }
}


v = videos.get('fin')
va = v.get('a')
vb = v.get('b')

video.cut(va.get('start'), va.get('duration'), va.get('video_in'), va.get('video_out'))
video.cut(vb.get('start'), vb.get('duration'), vb.get('video_in'), vb.get('video_out'))

filelist = [
    "file '{}'".format(va.get('video_out')),
    "file '{}'".format(vb.get('video_out'))
]

helpers.write_file(v.get('list'), filelist)
video.concat(v.get('list'), v.get('video_out'))
