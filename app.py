from flask import Flask, render_template, request
from config import config
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('app.html')

@app.route("/test.html")
def test():
    return render_template("test.html")

@app.route("/upload", methods=["POST"])
def upload():
	currTime = time.time()

	request.files["video"].save("uploads/video-"+str(currTime)+".webm")
	return "SUCCESS"

if __name__ == '__main__':
    app.run()
