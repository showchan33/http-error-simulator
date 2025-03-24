from flask import Flask
import time
import sys

app = Flask(__name__)

# 200が返る
@app.route("/")
def index():
  return "Hello, this is a simple HTTP error simulator!", 200

# 504が返る
@app.route("/slow")
def slow_response():
  time.sleep(5)
  return "This response took a long time", 200

# 502が返る
@app.route('/abort')
def abort():
  sys.exit(1)

# 500が返る(Flaskが500を返すので)
@app.route('/nothing')
def nothing():
  return None

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
