from __future__ import division, print_function

import os, random
import subprocess
import gc
import time
from model.models import Song, VideoClip

from flask import Flask, render_template, request, jsonify, send_file
from moviepy.editor import (VideoFileClip, concatenate_videoclips, AudioFileClip,
                            CompositeAudioClip)

from config import config

from bson import json_util

app = Flask(__name__)

FILLER_VIDEO = VideoFileClip("filler.mp4", audio=False)

def make_video(clips, song):
    end = 0

    for clip, lyric in zip(clips, song.lyrics):
        clip = VideoFileClip(clip)
        #if song == "Eye of the Tiger":
        #    lyric.start_time -= 2
        if end < lyric.start_time:  # GAP
            yield FILLER_VIDEO.speedx(final_duration=lyric.start_time - end)
        if clip.duration < lyric.duration:
            yield clip
            yield FILLER_VIDEO.speedx(final_duration=lyric.duration - clip.duration)
        else:
    	      yield clip.speedx(final_duration=lyric.duration)
        end = lyric.start_time + lyric.duration

def batch_concatenate(songs, batch_size=30):
    batch = []
    video = None
    timestamp = int(time.time())

    while True:
        try:
            if len(batch) > batch_size:
                video = concatenate_videoclips(batch)
                video.write_videofile("/tmp/video-{0}.mp4".format(timestamp))
                del video    # garbage collect the file descriptors!
                batch = [VideoFileClip("/tmp/video-{0}.mp4".format(timestamp))]
            batch.append(next(songs))
        except StopIteration:
            return concatenate_videoclips(batch)

@app.route('/play', methods=["POST"])
def play():
    song = Song.objects(title=request.json["song"]).get()

    video = batch_concatenate(make_video(request.json["clips"], song))
    instrumental = AudioFileClip("files/instrumental/{0}.wav".format(request.json["song"]))
    audio = CompositeAudioClip([video.audio, instrumental.subclip(0, video.duration)])

    fname = "output/output-{0}.webm".format(int(time.time()))
    video.set_audio(audio).write_videofile(fname)
    return send_file(fname, mimetype="video/webm")

@app.route('/auto_search', methods=['GET'])
def auto_search():
  search_term = request.args.get('term')
  results = Song.objects(title__icontains=search_term).distinct('title')
  return jsonify(list = results)

@app.route('/available_clips', methods=['GET'])
def available_clips():
  word = request.args.get('word')
  query = VideoClip.objects(word = word)
  return jsonify(clips = query.to_json())

@app.route('/', methods=['GET', 'POST'])
def home():
  should_show_results = (request.method == 'POST')
  if should_show_results:
    search_term = request.form['user_search']
    query = Song.objects(title = search_term)
    if query.count() == 0:
      return render_template('home.html', should_show_results = False,
        no_results_text = 'No results found')
    else:
      song = query.first()
      song_name = song.title
      artist_name = song.artist_name
      lyrics_list = map(lambda lyric : str(lyric.word), song.lyrics)
      lyrics = ' '.join(lyrics_list)
      return render_template('home.html', should_show_results = should_show_results,
        song_name = song_name, artist_name = artist_name, lyrics = lyrics)
  return render_template('home.html', should_show_results = should_show_results)

i = -1

def random_word():
  with open('files/eye_tiger.txt') as song_words:
    words = [line.rstrip('\n').lower() for line in song_words]
    word = words[i]
    return word

@app.route("/record")
def record():
    global i
    i += 1
    return render_template("record.html", word=random_word())


def detect_silence(sound, threshold=-40, chunk=5):
    trim = 0
    while sound[trim: trim + chunk].dBFS < threshold:
        trim += chunk
    return trim / 1000.0    # ms to s


@app.route("/upload", methods=["POST"])
def upload():
    curr = int(time.time())

    name = request.form["author_name"]
    word = request.form["word"]
    fname = "uploads/{0}-{1}.webm".format(word, curr)
    request.files["video"].save(fname)

    mp4_fname = "uploads/{0}-{1}.mp4".format(word, curr)
    subprocess.check_call(["ffmpeg", "-i", fname, "-qscale", "0", mp4_fname])
    video_clip = VideoClip(author=name, word=word, file_name=mp4_fname)
    video_clip.save()

    return "SUCCESS"

if __name__ == '__main__':
    app.run()
