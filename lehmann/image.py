#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import color
from ast import literal_eval as to_tuple
from glob import glob
from shutil import (
    copyfile, rmtree
)



def avg_color_data_original(images_format):
    result = {}
    _dict = {}
    _list = []

    for img in glob(images_format):
        avg = color.avg_color(img)
        if not _dict.has_key("{}{}{}".format(*avg)):
            _dict[ "{}{}{}".format(*avg) ] = img
            _list.append( avg )

    return (_list, _dict)


def build_set_original(_list, _dict):
    image_list = []
    for c_item in _list:
        complementary = color.complementary_rgb(c_item)
        closest_color = color.find_closest(complementary, _list)

        image_list.append(_dict.get("{}{}{}".format(*c_item)))
        image_list.append(_dict.get("{}{}{}".format(*closest_color)))

    return image_list


def avg_color_data(images_format):
    result = {}
    _dict = {}
    _list = []

    for img in glob(images_format):
        sys.stdout.write("\rProcessing: {}".format(img))
        sys.stdout.flush()
        pal = color.extract_palette(img,1)

        rgb_color = (0,0,0)
        try:
            rgb_color = map(to_tuple, color.in_format(pal, 'rgb'))[0]
            _list.append(rgb_color)
        except:
            pass

        if not _dict.has_key("{}".format(rgb_color)):
            _dict["{}".format(rgb_color)] = [img]
        else:
            _dict["{}".format(rgb_color)].append(img)


    print _dict

    return (_list, _dict)

def dom_color_data(images_format):
    result = {}
    _dict = {}
    _list = []

    for img in glob(images_format):
        sys.stdout.write("\rProcessing: {}".format(img))
        sys.stdout.flush()
        pal = color.dominant(img)

        rgb_color = pal
        # rgb_color = (0,0,0)
        # try:
        #     rgb_color = map(to_tuple, color.in_format(pal, 'rgb'))[0]
        #     _list.append(rgb_color)
        # except:
        #     pass

        if not _dict.has_key("{}".format(rgb_color)):
            _dict["{}".format(rgb_color)] = [img]
        else:
            _dict["{}".format(rgb_color)].append(img)


    print _dict

    return (_list, _dict)



def build_set(_list, _dict):
    image_list = []
    _list.sort(key=lambda rgb: color.rgb_to_hsv(rgb))
    for c_item in _dict:
        image_list += _dict.get("{}".format(c_item)) #.append(_dict.get("{}".format(c_item)))
    #     #complementary = color.complementary_rgb(c_item)
    #     #closest_color = color.find_closest(complementary, _list)

    #     #image_list.append(_dict.get("{}{}{}".format(*c_item)))
    #     #image_list.append(_dict.get("{}{}{}".format(*closest_color)))

    #     print c_item

    return image_list


def copy(image_list, image_dest, image_format):
    img_n=0
    for img in image_list:
        if os.path.isfile(img):
            copyfile(img,
                     os.path.join(image_dest,
                                  image_format % img_n))
        img_n += 1

    return None


def clean_cache(cache_dirs):
    map(rmtree, cache_dirs)


def make_cache(cache_dirs):
    map(os.makedirs, cache_dirs)
