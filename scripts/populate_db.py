#!/usr/bin/env python2
from __future__ import print_function
import os

from model.models import Lyric, Song, VideoClip
from lib.kar import Kar

def parse(fin):
    for line in fin:
        syllable, start, end = line.split()
        start = float(start)
        end = float(end)
        yield Lyric(word=syllable, start_time=start, duration=end-start)

if __name__ == '__main__':
    for fname in os.listdir("files/lyrics/"):
        song_name, __ = os.path.splitext(fname)

        song = Song(title=song_name)
        with open(os.path.join("files/lyrics/", fname)) as fin:
            song.lyrics = list(parse(fin))
        song.save()
