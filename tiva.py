#!/usr/bin/env python

"""
TIVA: TIVA Isn't Video Art
"""

import os
import argparse
import itertools
from tools import (
    video, fs
)
from textx.metamodel import metamodel_from_file

TV = metamodel_from_file('tools/grammar.tx', ignore_case=True)


class Video(object):
    def __init__(self, name):
        self.name = name
        self.actions = {
            'cut': ['start', 'duration', 'render', 'using'],
            'paste': ['using', 'render'],
            'blend': ['using', 'render'],
            'apply': ['using', 'fx', 'render']
        }

    def complies(self, action, args):
        "Just tries to find the expected words in the codeblock"
        expects = self.actions.get(action)
        does = filter(lambda is_valid: is_valid,
                      map(lambda e: e in args.keys(), expects))

        return len(does) == len(expects)

    def clean(self, vid):
        "Removes files"
        if isinstance(vid, (list, tuple, set)):
            map(self.clean, vid)
        else:
            fs.rm_files(vid)

    def action(self, action, args, verbose=False):
        "Performs an action based on the source code provided"
        if self.complies(action, args):

            if action == "cut":
                video.utils.cut(args.get('using').video,
                                args.get('render').video,
                                args.get('start').time,
                                args.get('duration').time,
                                verbose)

            if action == "paste":
                video.utils.glue(args.get('using').video,
                                 args.get('render').video,
                                 verbose)

            if action == "blend":
                video.fx.apply(
                    video.fx.blend,
                    args.get('using').video, args.get('render').video,
                    True,
                    verbose
                )

            if action == "apply":
                fx_list = map(video.fx.from_string, args.get('fx').list)

                video.fx.apply(
                    fx_list,
                    args.get('using').video, args.get('render').video,
                    False,
                    verbose
                )

            return args.get('using').video + [args.get('render').video]
        else:
            return None


def read(filename, clean=False, verbose=False):
    if os.path.isfile(filename):
        _model = TV.model_from_file(filename)
        v_name = os.path.splitext(os.path.basename(filename))[0]
        vid = Video(v_name)

        tmp_vids = []
        for act in _model.actions:
            tmp_vids += [vid.action(act.action,
                                    dict(using=act.using,
                                         render=act.render,
                                         start=act.start,
                                         every=act.every,
                                         duration=act.duration,
                                         fx=act.fx),
                                    verbose)]
        if clean:
            tmp_vids = list(itertools.chain.from_iterable(tmp_vids))
            vid.clean(set(tmp_vids[1:-1]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename',
                        type=str,
                        help="Use this source code")
    parser.add_argument('-c', '--clean',
                        action="store_true",
                        help="Removes all 'temporary' videos when finished")
    parser.add_argument('-V', '--verbose',
                        action="store_true",
                        help="Show stdout messages")

    args = parser.parse_args()
    if args.filename:
        read(args.filename,
             args.clean or False,
             args.verbose or False)
    else:
        print("{} -h".format(__file))
