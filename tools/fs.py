#!/usr/bin/env python

from os import makedirs
from os.path import (
    isfile, join
)
from shutil import (
    copyfile, rmtree
)


def copy(file_list, file_dest, file_format):
    "Copies files (ideally images) from here to there"
    img_n = 0
    for img in image_list:
        if isfile(img):
            copyfile(img,
                     join(image_dest,
                          image_format % img_n))
        img_n += 1

    return None


def rm_dir(dirs):
    "Removes directories"
    if isinstance(dirs, (list, tuple)):
        map(rm_dir, dirs)
    else:
        try:
            rmtree(dirs)
        except:
            pass


def rm_files(filelist):
    "Removes files"
    if isinstance(filelist, (list, tuple)):
        map(rm_files, filelist)
    else:
        try:
            os.remove(filename)
        except OSError:
            pass


def mk_dir(dirs):
    "Makes directories"
    if isinstance(dirs, (list, tuple)):
        map(mk_dir, dirs)
    else:
        try:
            makedirs(dirs)
        except:
            pass
