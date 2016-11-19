#!/usr/bin/env python

import sys
import color
from ast import literal_eval as to_tuple
from glob import glob
from helpers import pc


def color_data(images_path, by_type='avg', verbose=False):
    result = {}
    _dict = {}
    _list = []
    images = glob(images_path)
    total = len(images)

    n = 0
    for img in images:
        sys.stdout.write("\r {} of {} ({}%)".format(n, total, pc(n, total)))
        sys.stdout.flush()

        if by_type == 'avg':
            rgb_color = color.avg_color(img)
        elif by_type == 'dom':
            rgb_color = color.dominant(img)
        n += 1

        if rgb_color not in _dict.keys():
            _dict["{}".format(rgb_color)] = []

        _dict["{}".format(rgb_color)].append(img)

    return _dict


def build_set(_dict, sort_by='hsv'):
    image_list = []
    _list = _dict.keys()
    if sort_by == 'hls':
        _list.sort(key=lambda rgb: color.rgb_to_hls(to_tuple(rgb)))
    elif sort_by == 'hsl':
        _list.sort(key=lambda rgb: color.rgb_to_hsl(to_tuple(rgb)))
    elif sort_by == 'hsv':
        _list.sort(key=lambda rgb: color.rgb_to_hsv(to_tuple(rgb)))
    elif sort_by == 'lum':
        _list.sort(key=lambda rgb: color.luminance(to_tuple(rgb)))

    rgb_list = map(to_tuple, _list)
    for c_item in _list:
        image_list += _dict.get("{}".format(c_item))

    return image_list


def build_set_complementary(_dict, sort_by='hsv', every=4):
    image_list = []
    _list = _dict.keys()
    if sort_by == 'hls':
        _list.sort(key=lambda rgb: color.rgb_to_hls(to_tuple(rgb)))
    elif sort_by == 'hsl':
        _list.sort(key=lambda rgb: color.rgb_to_hsl(to_tuple(rgb)))
    elif sort_by == 'hsv':
        _list.sort(key=lambda rgb: color.rgb_to_hsv(to_tuple(rgb)))
    elif sort_by == 'lum':
        _list.sort(key=lambda rgb: color.luminance(to_tuple(rgb)))

    n = 0
    for c_item in _list:
        if n % every == 0:
            complementary = color.complementary_rgb(to_tuple(c_item))
            closest_color = color.find_closest(complementary,
                                               map(to_tuple, _list))
            image_list += _dict.get("{}".format(str(closest_color)))

        image_list += _dict.get("{}".format(c_item))
        n += 1

    return image_list
