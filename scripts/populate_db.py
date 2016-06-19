from model.models import Lyric, Song, VideoClip

def test_create_song():
    lyric1 = Lyric(word="Hey", start_time=0, duration=1)
    lyric2 = Lyric(word="Jude", start_time=1, duration=1)
    song = Song(title = "Hey Jude")
    song.lyrics.append(lyric1)
    song.lyrics.append(lyric2)
    song.save()

def fill_database():
    print "Filling in database..."
    # TODO: Alan will fill this in.

if __name__ == '__main__':
    test_create_song()
    # TODO: Uncomment this.
    # fill_database()
