from __future__ import division, print_function

import os, random
import time
from model.models import Song, VideoClip

from flask import Flask, render_template, request, jsonify, send_file
from moviepy.editor import (VideoFileClip, concatenate_videoclips, AudioFileClip,
                            CompositeAudioClip)

from config import config


app = Flask(__name__)

FILLER_VIDEO = VideoFileClip("filler.mp4", audio=False)

def make_video(clips, song):
    end = 0
    for clip, lyric in zip(clips, song.lyrics):
        print("ZZZ", end, lyric.start_time)
        if end < lyric.start_time:  # GAP
            print("QQQ", "GAP", lyric.start_time - end)
            yield FILLER_VIDEO.speedx(final_duration=lyric.start_time - end)
        print("QQQ", "NOP", lyric.duration)
    	yield clip.speedx(final_duration=lyric.duration)
        end = lyric.start_time + lyric.duration

@app.route('/play', methods=["POST"])
def play():
    clips = [VideoFileClip(clip) for clip in request.json["clips"]]
    song = Song.objects(title=request.json["song"]).get()

    video = concatenate_videoclips(list(make_video(clips, song)))
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

def random_word():
  with open('files/song_words.txt') as song_words:
    words = [line.rstrip('\n').split()[1] for line in song_words]
    word = words[random.randint(0,len(words)-1)]
    return word


words = ["imagine", "there's", "no", "heaven", "it's", "easy"]
i = -1

@app.route("/record")
def record():
    global i
    i += 1
    return render_template("record.html", word=words[i])

@app.route("/upload", methods=["POST"])
def upload():
    #import pdb; pdb.set_trace()
    currTime = time.time()

    name = request.form["author_name"]
    word = request.form["word"]
    file_extension = str(word) + "-" + str(currTime) + ".webm"
    file_name = "uploads/" + file_extension
    request.files["video"].save(file_name)
    
    video_clip = VideoClip(author = name, word = word, file_name = file_extension)
    video_clip.save()

    return "SUCCESS"

if __name__ == '__main__':
    app.run()
