#!/usr/bin/env python

from os import makedirs
from os.path import (
    isfile, join
)
from shutil import (
    copyfile, rmtree
)


def copy(image_list, image_dest, image_format):
    img_n=0
    for img in image_list:
        if isfile(img):
            copyfile(img,
                     join(image_dest,
                          image_format % img_n))
        img_n += 1

    return None


def rm_dir(dirs):
    if isinstance(dirs, (list, tuple)):
        map(rm_dir, dirs)
    else:
        try:
            rmtree(dirs)
        except:
            pass


def mk_dir(dirs):
    if isinstance(dirs, (list, tuple)):
        map(mk_dir, dirs)
    else:
        try:
            makedirs(dirs)
        except:
            pass
