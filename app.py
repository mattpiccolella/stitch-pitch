from flask import Flask, render_template, request, jsonify
from config import config
from model.models import Song

app = Flask(__name__)

@app.route('/auto_search', methods=['GET'])
def auto_search():
  search = request.args.get('term')
  results 
  return jsonify(list = RESULTS)

@app.route('/', methods=['GET', 'POST'])
def home():
  should_show_results = (request.method == 'POST')
  # TODO: Make these real.
  song_name = 'Hey Jude'
  artist_name = 'The Beatles'
  lyrics = "Hey Jude, don't make it bad, take a sad song, and make it better"
  return render_template('home.html', should_show_results = should_show_results,
    song_name = song_name, artist_name = artist_name, lyrics = lyrics)

if __name__ == '__main__':
    app.run()