from flask import Flask, render_template
from config import config

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('app.html')

if __name__ == '__main__':
    app.run()