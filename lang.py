#!/usr/bin/env python

import os
import re
import argparse
import tempfile
import operator as op

from utils import video


__file = os.path.basename(__file__)
TEMP_DIR = tempfile.mkdtemp("-lang")
CACHE_DIR = os.path.join(TEMP_DIR, "cache")


PARSECODE_RE = "(?P<action>\w+)\s?{(?P<codeblock>.[^}]*)}"
PARSECODE = re.compile(PARSECODE_RE, re.DOTALL)

PARSEBLOCK_RE = "(?P<fn>\w+)\s\"(?P<param>.[^\"]*)\""
PARSEBLOCK = re.compile(PARSEBLOCK_RE, re.DOTALL)

PARSEFX_RE = "(?P<param>\w[^:]+):?(?P<value>.*)"
PARSEFX = re.compile(PARSEFX_RE, re.DOTALL)


ENV = {
    'cut': dict(
        type='action',
        expects=['start', 'duration', 'render', 'using']
    ),
    'glue': dict(
        type='action',
        expects=['using', 'render']
    ),
    'apply': dict(
        type='action',
        expects=['using', 'fx', 'render']
    ),
    'using': dict(
        type='var',
        expects=[str]
    ),
    'start': dict(
        type='var',
        expects=[str, int, float]
    ),
    'during': dict(
        type='var',
        expects=[str, int, float]
    ),
    'fx': dict(
        type='var',
        expects=[str]
    ),
    'render': dict(
        type='var',
        expects=[str]
    ),
}


EXAMPLES = {
    'cut': """
{
  using "video_orig.mp4"
  start "00:00:00"
  duration "00:00:10"
  render "video_a.mp4"
}""",
    'glue': """
{
  using "video_a.mp4"
  using "video_b.mp4"
  render "video_glued.mp4"
}""",
    'apply': """
{
  using "video_glued.mp4"
  fx "lehmann"
  render "video_lehmann.mp4"
}""",
}


def get_example(action):
    "Tries to give an example of how to use an `action`"
    if EXAMPLES.has_key(action):
        return EXAMPLES.get(action)
    else:
        return "No example available, sorry :("


def raise_error(action, codeblock):
    raise SyntaxError("""
`{action}` codeblock has a syntax error
Should look like:
{example}

But looks like:
_OB_
{codeblock}
_CB_
""".format(action=action,
           example=get_example(action),
           codeblock=codeblock).replace('_OB_','{').replace('_CB_','}'))


def interpret(action, codeblock):
    video_in = video_out = start = duration = ""
    fx = []
    py_code = []
    for fn, param in PARSEBLOCK.findall(codeblock):
        fn = fn.strip()
        param = param.strip()

        if fn == "using":
            video_in = param

        if fn == "render":
            video_out = param

        if fn == "start":
            start = param

        if fn == "duration":
            duration = param

        if fn == 'fx':
            fx += [PARSEFX.findall(param)[0]]

        py_code += [
            ""
        ]
        print "fn `{}` with `{}`".format(fn, param)


def complies(action, codeblock):
    "Just tries to find the expected words in the codeblock"
    expects = ENV.get(action).get('expects')
    block = [fn for fn, param in PARSEBLOCK.findall(codeblock)]
    does = filter(lambda is_valid: is_valid,
                   map(lambda e: e in block, expects))

    return len(does) == len(expects)


def read(filename, verbose):
    "Reads the code and renders a video"
    program = " ".join(open(filename, 'r').readlines())

    py_code = []
    for action, codeblock in PARSECODE.findall(program):
        print "will ", action
        if complies(action, codeblock):
            interpret(action, codeblock)
        else:
            raise_error(action, codeblock)

        #print video_in, video_out, start, duration, fx
        #print "*"*80

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename',
                        type=str,
                        help="Use this source code")
    parser.add_argument('-V', '--verbose',
                        action="store_true",
                        help="Show stdout messages")

    args = parser.parse_args()
    if args.filename:
        read(args.filename,
             args.verbose or False)
    else:
        print("{} -h".format(__file))
