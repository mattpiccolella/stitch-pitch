#!/usr/bin/env python2
from __future__ import print_function
import os

from model.models import Lyric, Song, VideoClip
from lib.kar import Kar

FILE_NAME_EXT = '.mp3'

def parse(fin):
    for line in fin:
        syllable, start, end = line.split()
        start = float(start)
        end = float(end)
        yield Lyric(word=syllable, start_time=start, duration=end-start)

if __name__ == '__main__':
    for fname in os.listdir("files/lyrics/"):
        song_name, __ = os.path.splitext(fname)
        file_name = song_name + FILE_NAME_EXT

        song = Song(title=song_name, file_name = file_name)
        with open(os.path.join("files/lyrics/", fname)) as fin:
            song.lyrics = list(parse(fin))
        song.save()
