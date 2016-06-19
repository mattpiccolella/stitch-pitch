#!/usr/bin/env python2
from __future__ import print_function
import os

from model.models import Lyric, Song, VideoClip
from lib.kar import Kar

def add_kar(song_name, fname):
    k = Kar(fname)
    song = Song(title=song_name)
    song.lyrics = [Lyric(word=syllable.text,
                         start_time=syllable.start,
                         duration=syllable.duration)
                   for syllable in k.lyrics]
    song.save(force_insert=True)

if __name__ == '__main__':
    for fname in os.listdir("files/kar/"):
        song_name, __ = os.path.splitext(fname)
        fname = os.path.join("files/kar/", fname)
        try:
            add_kar(song_name, fname)
            print(song_name)
        except Exception as e:
            print()
            print(song_name, "failed")
            print(e)
            print()
