import json

import storage

from flask import Flask, url_for, request
app = Flask(__name__)

@app.route("/")
def main():
  with open("static/index.html") as f:
    return f.read()

# apis
@app.route("/api/find")
def find():
  return ""

@app.route("/api/def/<word>/add", methods=["POST", "PUT"])
def add_def(word):
  data = storage.get_def(word)
  print data
  if not data:
    data = []
  d = json.loads(request.data)
  if not d or "def" not in d:
    return json.dumps({"status": "error"})
  data.append({"def": d["def"].strip()})
  storage.set_def(word, data)
  return json.dumps({"status": "worked"})

@app.route("/api/def/<word>", methods=["GET", "POST"])
@app.route("/api/def/<word>/", methods=["GET", "POST"])
def single_word(word):
  return json.dumps(storage.get_def(word))

@app.route("/api/all_defs")
@app.route("/api/all_defs/")
def all_words():
  return json.dumps(storage.get_all_def())

if __name__ == "__main__":
  app.run(debug=True)
  url_for("static", filename='index.html')
  url_for("static", filename='js/jquery.min.js')
  url_for("static", filename='js/bootstrap.min.js')
  url_for("static", filename='js/ICanHaz.min.js')
  url_for("static", filename='css/bootstrap.css')
