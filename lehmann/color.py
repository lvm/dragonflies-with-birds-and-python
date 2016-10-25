#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import re
import colorsys
import subprocess as sp
from math import sqrt

from colorthief import ColorThief

color_match_re = "(\d+),(\d+),(\d+)"
palette_match_re = "(?P<px>\d+): (?P<rgb>.*) (?P<hex>#[0-9a-f]{6}) (?P<srgb>s?rgb\(\d+,\d+,\d+\))"
remove_rgb_re = "(s?rgb\(|\))"


steve_hollasch_table = {'153,50,204': 'orchid_dark', '85,107,47': 'olive_green_dark', '253,245,230': 'old_lace', '106,90,205': 'slate_blue', '250,235,215': 'antique_white', '128,42,42': 'brown', '135,206,250': 'sky_blue_light', '255,255,0': 'yellow', '255,99,71': 'tomato', '46,71,59': 'lamp_black', '0,255,0': 'green', '255,97,3': 'cadmium_orange', '60,179,113': 'sea_green_medium', '47,79,79': 'slate_grey_dark', '176,23,31': 'indian_red', '123,104,238': 'slate_blue_medium', '115,61,26': 'deep_ochre', '255,248,220': 'cornsilk', '64,224,208': 'turquoise', '0,255,127': 'spring_green', '255,228,196': 'bisque', '255,255,240': 'ivory', '145,33,158': 'cobalt_violetdeep', '139,69,19': 'saddle_brown', '0,0,205': 'blue_medium', '189,252,201': 'mint', '72,61,139': 'slate_blue_dark', '97,179,41': 'cinnabar_green', '252,255,240': 'titanium_white', '128,128,105': 'warm_grey', '255,160,122': 'light_salmon', '255,153,18': 'cadmium_yellow', '0,0,0': 'black', '210,180,140': 'tan', '253,248,255': 'zinc_white', '94,38,5': 'van_dyke_brown', '218,165,32': 'goldenrod', '46,139,87': 'sea_green', '10,201,43': 'permanent_green', '94,38,18': 'sepia', '189,183,107': 'khaki_dark', '250,128,114': 'salmon', '240,230,140': 'khaki', '160,82,45': 'sienna', '173,255,47': 'green_yellow', '221,160,221': 'plum', '255,228,181': 'moccasin', '255,255,255': 'white', '61,89,171': 'cobalt', '112,128,144': 'slate_grey', '41,36,33': 'ivory_black', '240,248,255': 'alice_blue', '143,188,143': 'sea_green_dark', '250,240,230': 'linen', '0,191,255': 'sky_blue_deep', '32,178,170': 'sea_green_light', '70,130,180': 'steel_blue', '25,25,112': 'midnight_blue', '92,36,110': 'ultramarine_violet', '245,245,245': 'white_smoke', '107,142,35': 'olive_drab', '56,94,15': 'terre_verte', '255,250,250': 'snow', '143,94,153': 'violet', '255,182,193': 'pink_light', '115,74,18': 'raw_umber', '255,168,36': 'aureoline_yellow', '227,54,56': 'rose_madder', '176,224,230': 'powder_blue', '255,255,224': 'yellow_light', '127,255,212': 'aquamarine', '30,144,255': 'dodger_blue', '105,105,105': 'dim_grey', '0,0,255': 'blue', '216,191,216': 'thistle', '8,46,84': 'indigo', '127,255,0': 'chartreuse', '0,250,154': 'spring_greenmedium', '227,23,13': 'cadmium_red_deep', '255,227,3': 'cadmium_lemon', '255,168,18': 'naplesyellowdeep', '255,105,180': 'hot_pink', '227,130,23': 'yellow_ochre', '255,250,240': 'floral_white', '227,168,105': 'melon', '237,145,33': 'carrot', '240,255,240': 'honeydew', '176,196,222': 'steel_blue_light', '255,0,255': 'magenta', '255,240,245': 'lavender_blush', '59,94,43': 'olive', '192,192,192': 'grey', '205,133,63': 'peru', '176,48,96': 'maroon', '219,41,41': 'brown_madder', '255,128,0': 'orange', '248,248,255': 'ghost_white', '34,139,34': 'forest_green', '219,112,147': 'violet_red_pale', '50,205,50': 'lime_green', '224,255,255': 'cyan_white', '219,38,69': 'permanent_violet', '255,61,13': 'greenish_umber', '212,26,31': 'venetian_red', '245,245,220': 'light_beige', '119,136,153': 'slate_grey_light', '227,46,48': 'madder_lake_deep', '188,143,143': 'rosy_brown', '255,245,238': 'seashell', '240,255,255': 'azure', '128,138,135': 'cold_grey', '227,112,26': 'mars_yellow', '135,66,31': 'brown_ochre', '0,201,87': 'emerald_green', '220,220,220': 'gainsboro', '0,255,255': 'cyan', '138,54,15': 'burnt_sienna', '244,164,96': 'sandy_brown', '124,252,0': 'lawn_green', '255,125,64': 'flesh', '199,97,20': 'raw_sienna', '154,205,50': 'yellow_green', '255,127,80': 'coral', '199,120,38': 'gold_ochre', '148,0,211': 'violet_dark', '95,158,160': 'cadet', '211,211,211': 'light_grey', '51,161,201': 'peacock', '147,112,219': 'purple_medium', '255,228,225': 'misty_rose', '255,0,0': 'red', '160,32,240': 'purple', '72,209,204': 'turquoise_medium', '199,21,133': 'violet_redmedium', '255,215,0': 'gold', '252,230,201': 'eggshell', '238,221,130': 'light_goldenrod', '238,232,170': 'goldenrod_pale', '250,250,210': 'goldenrod_light', '0,206,209': 'turquoise_dark', '227,18,48': 'geranium_lake', '152,251,152': 'green_pale', '0,0,128': 'navy', '230,230,250': 'lavender', '255,235,205': 'blanched_almond', '102,205,170': 'aquamarinemedium', '173,216,230': 'blue_light', '61,145,64': 'cobalt_green', '135,206,235': 'sky_blue', '227,38,54': 'alizarin_crimson', '175,238,238': 'turquoise_pale', '0,100,0': 'green_dark', '255,140,0': 'dark_orange', '222,184,135': 'burlywood', '3,168,158': 'manganese_blue', '245,255,250': 'mint_cream', '18,10,143': 'ultramarine', '208,32,144': 'violet_red', '150,69,20': 'mars_orange', '100,149,237': 'cornflower', '245,222,179': 'wheat', '255,3,13': 'cadmium_red_light', '138,43,226': 'blue_violet', '65,105,225': 'royal_blue', '255,87,33': 'flesh_ochre', '48,128,20': 'sap_green', '227,207,87': 'banana', '255,222,173': 'navajo_white', '255,192,203': 'pink', '102,128,20': 'chromeoxidegreen', '255,239,213': 'papaya_whip', '186,85,211': 'orchid_medium', '212,61,26': 'english_red', '0,199,140': 'turquoise_blue', '110,255,112': 'viridian_light', '132,112,255': 'slate_blue_light', '184,134,11': 'goldenrod_dark', '156,102,31': 'brick', '135,38,87': 'raspberry', '255,250,205': 'lemon_chiffon', '178,34,34': 'firebrick', '163,148,128': 'beige', '138,51,36': 'burnt_umber', '218,112,214': 'orchid', '255,218,185': 'peach_puff', '240,128,128': 'coral_light', '255,69,0': 'orange_red', '255,20,147': 'deep_pink', '210,105,30': 'chocolate', '5,184,204': 'cerulean'}


###
#
# FUNCS
#

def dominant(image):
    "Obtains the dominant color of a single image using `color-thief-py`"
    color_thief = ColorThief(image)
    return color_thief.get_color(quality=1)


def avg_color(image):
    "Obtains the average color of a single image using imagemagick's `convert`"
    color = sp.check_output(['convert', image, '-scale', ' 1x1\!',
                             '-format',
                             '"%[fx:int(255*r+.5)],%[fx:int(255*g+.5)],%[fx:int(255*b+.5)]"', 'info:-'])

    if color:
        color = re.findall(color_match_re, color)[0]
    return tuple(map(lambda c: int(c), (color)))


def extract_palette(image, n_colors=16):
    "Extracts a single image palette using imagemagick's `convert`"
    palette = sp.check_output(['convert', image, '-colors', str(n_colors),
                               '-depth', '8', '-format', "%c", 'histogram:info:'])
    palette = map(lambda l: l.lower(), map(lambda l: l.strip(), palette.split("\n")))
    return filter(lambda c: c, palette)


def match_format(line):
    "Returns a list of matches given a certain reg exp. see code."
    return re.match(palette_match_re, line)


def in_format(palette, format):
    "Returns a list of matches given a certain format (rgb or hex)"
    color_list = map(lambda l: match_format(l), palette)

    return map(lambda cl: cl.group(format), color_list)



def get_distance(rgb_a, rgb_b):
    "Calculates the distance between two colors using Euclidean Distances"
    return sqrt(sum([(c1-c2)**2 for c1, c2 in zip(rgb_a, rgb_b)]))


def find_close(color, color_list):
    "Find close colors in a list based on `get_distance`"
    return sorted(color_list, key=lambda c: get_distance(c, color))


def find_closest(color, color_list):
    "Find the closest color based on `get_distance`"
    return find_close(color, color_list)[0]


###
#
# CONVERSION
#



def cmy_to_cmyk(color):
    "Converts a CMY to a CMYK color"
    c, m, y = color
    k = 1
    if c < k:
        k = c
    if m < k:
        k = m
    if y < k:
        k = y
    if k < 1:
        c, m, y = 0, 0, 0
    else:
        c = (c-k) / (1-k)
        m = (m-k) / (1-k)
        y = (y-k) / (1-k)

    return c, y, m, k


def _rgb256_to_rgb(color):
    "Converts a color from RGB to HSV"
    return map(lambda c: c/255, color)


def _rgb_to_rgb256(color):
    "Converts a color from RGB to HSV"
    return tuple(map(lambda c: int(c*255), color))


def rgb_to_hsv(color):
    "Converts a color from RGB to HSV"
    return colorsys.rgb_to_hsv(*_rgb256_to_rgb(color))


def rgb_to_hls(color):
    "Converts a color from RGB to HSV"
    return colorsys.rgb_to_hls(*_rgb256_to_rgb(color))


def rgb_to_hsl(color):
    "Converts a color from RGB to HSL"
    h, l, s = colorsys.rgb_to_hls(*_rgb256_to_rgb(color))
    return h,s,l


def hsv_to_rgb(color):
    "Converts a color from HSV to RGB (0..1)"
    return colorsys.hsv_to_rgb(*color)

def hsv_to_rgb256(color):
    "Converts a color from HSV to RGB (0..255)"
    return _rgb_to_rgb256(colorsys.hsv_to_rgb(*color))


###
#
# PALETTES
#


def palette_rgb(palette, format_256=True):
    "Returns a list of colors in (s)RGB format"
    color_list = in_format(palette, "srgb")
    color_list = map(lambda c: re.sub(remove_rgb_re, "", c).split(","),
                      color_list)
    color_list = [tuple(map(lambda c: int(c), color)) for color in color_list]

    if not format_256:
        color_list = [tuple(map(lambda c: c/255, rgb)) for rgb in color_list]

    return color_list


def palette_cmy(palette):
    "Returns a list of colors in CMY format"
    return [colorsys.rgb_to_hsv(1-r,1-g,1-b)  for r,g,b in palette_rgb(palette, False)]


def palette_cmyk(palette):
    "Returns a list of colors in CMYK format"
    return map(lambda c: cmy_to_cmyk(c), color_cmy(palette))


def palette_hex(palette, no_hash=True):
    "Returns a list of colors in Hex format"
    if no_hash:
        return map(lambda c: c.replace("#",""), in_format(palette, "hex"))
    else:
        return in_format(palette, "hex")


def palette_hsv(palette):
    "Returns a list of colors in HSV format"
    return [rgb_to_hsv(rgb)  for rgb in palette_rgb(palette)]


def palette_hls(palette):
    "Returns a list of colors in HLS format"
    return [rgb_to_hls(rgb)  for rgb in palette_rgb(palette)]


def palette_hsl(palette):
    "Returns a list of colors in HLS format"
    return [(h,s,l)  for h,l,s in palette_hls(palette)]


def palette_descriptive(palette):
    "Returns a list of descriptive names for colors according to Steve Hollasch"
    return [steve_hollasch_table.get("{},{},{}".format(r,g,b)) for r,g,b in palette_rgb(palette)]


###
#
# GROUPS
#


def monochromatic(color):
    "Returns its argument. Lazy AF."
    return color


def complementary_hsv(color, in_pc=True):
    "Returns a complementary color given a color in HSV format"
    h,s,v = color
    h =  (h * 360) + 180
    if h > 360:
        h = h - 360

    if in_pc:
        return h, s * 100,v * 100
    else:
        return h, s, v


def complementary_rgb(color, format_256=True):
    "Returns a complementary color given a color in RGB format"
    h, s, v = complementary_hsv(rgb_to_hsv(color))
    if format_256:
        return hsv_to_rgb256((h/360, s/100, v/100))
    else:
        return hsv_to_rgb((h/360, s/100, v/100))



def triad_hsv(color, in_pc=True):
    "Returns a triad color given a color in HSV format"
    h,s,v = color
    _h = 0
    triad = []
    # if orig = 0 deg then comp = 180 deg thus [180-60, 180+60]
    for angle in [120, 240]:
        _h =  (h * 360) + angle
        if _h > 360:
            _h = _h - 360

        if in_pc:
            triad.append( (_h, s * 100, v * 100) )
        else:
            triad.append( (_h, s, v) )

    return triad


def triad_rgb(color, format_256=True):
    "Returns a triad color given a color in RGB format"
    triad = triad_hsv(rgb_to_hsv(color))
    if format_256:
        return map(lambda t:
                   hsv_to_rgb256((t[0]/360, t[1]/100, t[2]/100)),
                   triad)
    else:
        return map(lambda t:
                   hsv_to_rgb((t[0]/360, t[1]/100, t[2]/100)),
                   triad)
