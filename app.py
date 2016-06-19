from flask import Flask, render_template, request, jsonify
from config import config
import time
from model.models import Song, VideoClip

app = Flask(__name__)

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
    with open('files/song_words.txt') as song_words:
      words = [line.rstrip('\n').split()[1] for line in song_words]
      words_string = ' '.join(words)
      return render_template("record.html", words = words_string)

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
