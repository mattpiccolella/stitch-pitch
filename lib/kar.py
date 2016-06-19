from __future__ import absolute_import
from collections import namedtuple

from . import midifile

Syllable = namedtuple("Syllable", ["text", "start", "duration"])

class Kar(object):
    """Interface to karaoke .kar files

    Args:
        fin (str): Filename of .kar file to open
    Attributes:
        midi (midifile.midifile): Internal class from Karapython
    """
    def __init__(self, fin):
        self.midi = midifile.midifile()
        self.midi.load_file(fin)

        assert self.midi.karfile, "Karaoke file does not have lyrics"

    @property
    def lyrics(self):
        syllables = list(self.midi.karsyl)
        times = list(self.midi.kartimes)
        lyrics = [Syllable(syllable, start, end - start)
                  for syllable, start, end, in zip(syllables, times, times[1:])]
        # Get last syllable
        last_duration = min(times[-1] - self.midi.notes[-1][5], 0.5)
        lyrics.append(Syllable(syllables[-1], times[-1], last_duration))

        return lyrics
