from __future__ import division

import os
import time

from flask import Flask, render_template, request, jsonify, send_file
from moviepy.editor import VideoFileClip, concatenate_videoclips

from config import config
from model.models import Song


app = Flask(__name__)

# FILLER_VIDEO = meditor.VideoFileClip("filler.mp4", audio=False)

def make_video(clips, song):
    prev_finish = 0
    for clip, lyric in zip(clips, song.lyrics):
        if prev_finish < lyric.start_time:  # GAP
            length = lyric.start_time - prev_finish
            yield FILLER_VIDEO.subclip(0, length) \
                              .set_start(prev_finish)
        else:
            yield clip.speedx(final_duration=lyric.duration)
        prev_finish = lyric.start_time + lyric.duration

@app.route('/play', methods=["POST"])
def play():
    clips = [meditor.VideoFileClip(clip) for clip in request.json["clips"]]
    song = Song.object(song_name=request.json["song"])

    video = concatenate_videoclips(list(make_video(clips, song)))

    fname = "output-{0}.webm".format(int(time.time()))
    video.write_videofile(fname)
    send_file(fname, mimetype="video/webm")

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

@app.route("/record")
def record():
    return render_template("record.html", word="hello")

@app.route("/upload", methods=["POST"])
def upload():
	currTime = time.time()

	request.files["video"].save("uploads/video-"+str(currTime)+".webm")
	return "SUCCESS"

if __name__ == '__main__':
    app.run()
