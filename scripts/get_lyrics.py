#!/usr/bin/env python2
from __future__ import print_function
import os

from model.models import Lyric, Song, VideoClip
from lib.kar import Kar

if __name__ == '__main__':
    for fname in os.listdir("files/kar/"):
        song_name, __ = os.path.splitext(fname)
        fname = os.path.join("files/kar/", fname)
        try:
            k = Kar(fname)
            print(song_name)
            with open("files/lyrics/" + song_name, "w") as fout:
                fout.write("\n".join(" ".join([text, str(start), str(duration)])
                                     for text, start, duration in k.lyrics))

        except Exception as e:
            print()
            print(song_name, "failed")
            print(e)
            print()
