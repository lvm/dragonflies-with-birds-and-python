#!/usr/bin/env python

import os
import argparse
from tools import video
from textx.metamodel import metamodel_from_file

TV = metamodel_from_file('tools/grammar.tx', ignore_case=True)

class Video(object):
    def __init__(self, name):
        self.name = name
        self.actions = {
            'cut': ['start', 'duration', 'render', 'using'],
            'glue': ['using', 'render'],
            'apply': ['using', 'fx', 'render']
        }


    def complies(self, action, args):
        "Just tries to find the expected words in the codeblock"
        expects = self.actions.get(action)
        does = filter(lambda is_valid: is_valid,
                      map(lambda e: e in args.keys(), expects))

        return len(does) == len(expects)


    def action(self, action, args, verbose=False):
        if self.complies(action, args):
            if action == "cut":
                video.utils.cut(args.get('using').video, args.get('render').video,
                                args.get('start').time, args.get('duration').time,
                                verbose)

            if action == "glue":
                video.utils.glue(args.get('using').video, args.get('render').video,
                                 verbose)

            if action == "apply":
                video.fx.apply(
                    map(video.fx.from_string, args.get('fx').list),
                    args.get('using').video, args.get('render').video,
                    verbose
                )

            return args.get('render').video
        else:
             return None


def read(filename, verbose):
    if os.path.isfile(filename):
        _model = TV.model_from_file(filename)
        v_name = os.path.splitext(os.path.basename(filename))[0]
        video = Video(v_name)

        for act in _model.actions:
            video.action(act.action,
                         dict(using=act.using,
                              render=act.render,
                              start=act.start,
                              duration=act.duration,
                              fx=act.fx),
                         verbose)


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
