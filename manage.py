import os

import click

from model.models import Song, Lyric
from lib.kar import Kar

@click.group()
def cli():
    pass

@cli.command()
def delete():
    Song.drop_collection()

def parse(fin):
    for line in fin:
        word, start, end = line.split()
        start = float(start)
        end = float(end)
        yield Lyric(word=word.lower(), start_time=start,
                    duration=end - start)

ARTIST_NAME =  {
    'Blackbird': 'The Beatles',
    'Eye of the Tiger': 'Survivor',
    'New York, New York': 'Frank Sinatra',
    'Wonderful World': 'Louis Armstrong',
    'Help': 'The Beatles',
    'Hey Jude': 'The Beatles',
    'Mrs Robinson': 'Simon and Garfunkel',
    'Take Me Out to the Ballgame': 'Anonymous',
    'Imagine': 'John Lennon'
}

@cli.command()
def load_lyrics():
    for fname in os.listdir("files/lyrics/"):
        song_name, __ = os.path.splitext(fname)
        file_name = song_name + ".mp3"
        artist_name = ARTIST_NAME[song_name]

        song = Song(title=song_name, file_name=file_name,
                    artist_name=artist_name)
        with open(os.path.join("files/lyrics/", fname)) as fin:
            song.lyrics = list(parse(fin))
        song.save()

@cli.command()
def display():
    print("\n".join(song.title for song in Song.objects))

if __name__ == "__main__":
    cli()
