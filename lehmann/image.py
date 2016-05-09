#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import color
from glob import glob
from shutil import (
    copyfile, rmtree
)


def avg_color_data(images_format):
    result = {}
    _dict = {}
    _list = []

    for img in glob(images_format):
        avg = color.avg_color(img)
        if not _dict.has_key("{}{}{}".format(*avg)):
            _dict[ "{}{}{}".format(*avg) ] = img
            _list.append( avg )

    return (_list, _dict)


def build_set(_list, _dict):
    image_list = []
    for c_item in _list:
        complementary = color.complementary_rgb(c_item)
        closest_color = color.find_closest(complementary, _list)

        image_list.append(_dict.get("{}{}{}".format(*c_item)))
        image_list.append(_dict.get("{}{}{}".format(*closest_color)))

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
