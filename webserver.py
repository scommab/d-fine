import json
import uuid
import logging
from datetime import datetime

import storage

import markdown
from flask import Flask, url_for, request
app = Flask(__name__)

logging.basicConfig(filename='d-fine.log', level=logging.DEBUG)

def parse_request():
  word = request.args.get("word", None)
  pos = request.args.get("def", None)
  return word, pos

@app.route("/")
def main():
  with open("static/index.html") as f:
    return f.read()

# apis
@app.route("/api/def/find/")
def find():
  contains = request.args.get("contains", None)
  startswith = request.args.get("startswith", None)
  endswith = request.args.get("endswith", None)
  data = storage.get_all_def()
  if contains:
    data = [d for d in data if contains in d]
  if startswith:
    data = [d for d in data if d.startswith(startswith)]
  if endswith:
    data = [d for d in data if d.endswith(endswith)]

  return json.dumps({
    "status": "worked",
    "data": data
  })

@app.route("/api/def/add/", methods=["POST", "PUT"])
def add_def():
  word, pos = parse_request()
  data = storage.get_def(word)
  if not data:
    data = []
  d = json.loads(request.data)
  if not d or "def" not in d:
    return json.dumps({
      "status": "error",
      "message":"Incorrect or no Data sent"
    })
  def_data = {
    "id": str(uuid.uuid4()),
    "def": d["def"].strip(),
    "html": markdown.markdown(d["def"], safe_mode='escape'),
    "last_touch": datetime.now().isoformat()
    }
  if pos is None or pos == "":
    data.append(def_data)
  else:
    def_data["id"] = pos
    found = False
    for d, i in zip(data, range(len(data))):
      if d["id"] == pos:
        data[i] = def_data
        found = True
        break
    if not found:
      return json.dumps({
        "status": "error",
        "message": "the def '%s' was not found" % pos 
      })

  storage.set_def(word, data)
  return json.dumps({"status": "worked"})

@app.route("/api/def/del/", methods=["POST", "PUT"])
def del_def():
  word, pos = parse_request()
  data = storage.get_def(word)
  if not data:
    return json.dumps({
      "status": "error",
      "message":"word is already deleted"
    })
  for i in range(len(data)):
    d = data[i]
    if d["id"] == pos:
      del data[i]
      break
  if len(data) == 0:
    storage.del_def(word)
  else:
    storage.set_def(word, data)
  return json.dumps({"status": "worked"})


@app.route("/api/def/get/")
def single_word_def():
  word, pos = parse_request()
  data = storage.get_def(word)
  if not data:
    logging.debug("LOOK UP FAILED: %s" % word)
    storage.failed_lookup(word)
    return json.dumps({
      "status": "error",
      "message": "Coudn't find '%s'" % (word)
    })
  if not pos:
    logging.debug("LOOK UP WORKED: %s" % word)
    return json.dumps({
      "status": "worked",
      "word": word,
      "defs": data
    });
  result = None
  for d in data:
    if d["id"] == pos:
      result = d
      break
  if not result:
    logging.debug("LOOK UP WITH POS FAILED: %s (%s)" % (word, pos))
    return json.dumps({
      "status": "error",
      "message": "Coudn't find '%s' with def '%s'" % (word, pos)
    })
  logging.debug("LOOK UP WORKED: %s (%s)" % (word, pos))
  return json.dumps({
    "status": "worked",
    "word": word,
    "def": result
  });


@app.route("/api/failed/get/")
def failed_lookups():
  r = storage.get_failed_lookup()
  return json.dumps({
    "status": "wroked",
    "words": r
    })

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
  url_for("static", filename='index.html')
  url_for("static", filename='js/jquery.min.js')
  url_for("static", filename='js/shodow.js')
  url_for("static", filename='js/bootstrap.min.js')
  url_for("static", filename='js/ICanHaz.min.js')
  url_for("static", filename='css/bootstrap.css')
