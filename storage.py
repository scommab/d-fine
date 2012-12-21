import json

import redis

class mockRedis(object):
  def __init__(self):
    self.keystore = {}

  def hget(self, name1, name2):
    return self.keystore.get(name1, {}).get(name2, None)

  def hset(self, name1, name2, val):
    d = self.keystore.get(name1, {})
    d[name2] = val
    self.keystore[name1] = d

  def hkeys(self, name1):
    return self.keystore.get(name1, {}).keys()

DEBUG = True
    
mock = mockRedis()
def get_connection():
  if DEBUG:
    return mock
  try:
    return redis.Redis()
  except:
     #debug mode
    return mock

def get_def(name):
  d = get_connection().hget("jargon-defs", name)
  if not d:
    return d
  return json.loads(d)

def get_all_def():
  return get_connection().hkeys("jargon-defs")

def set_def(name, defs):
  return get_connection().hset("jargon-defs", name, json.dumps(defs))

if __name__ == "__main__":
  DEBUG = True
  print get_def("nothing") == None
  set_def("test", {"test": 1})
  print get_def("test")["test"] == 1
  set_def("test", {"test": 2})
  print get_def("test")["test"] == 2
  set_def("test2", {"test": 0})
  print get_all_def()
