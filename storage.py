import json

import redis

class mockRedis(object):
  def __init__(self):
    self.keystore = {}

  def hget(self, name1, name2):
    return self.keystore.get(name1, {}).get(name2, None)

  def hdel(self, name1, name2):
    if name1 in self.keystore:
      if name2 in self.keystore[name1]:
        del self.keystore[name1][name2]

  def hset(self, name1, name2, val):
    d = self.keystore.get(name1, {})
    d[name2] = val
    self.keystore[name1] = d

  def hincrby(self, name1, name2, val):
    old = self.hget(name1, name2)
    if old is None:
      self.hset(name1, name2, val)
    else:
      self.hset(name1, name2, old+val)

  def hgetall(self, name1):
    return self.keystore.get(name1, {})

  def hkeys(self, name1):
    return self.keystore.get(name1, {}).keys()

DEBUG = None
    
mock = mockRedis()
def get_connection():
  global DEBUG
  if DEBUG is None:
    try:
      r = redis.Redis()
      r.ping()
      DEBUG = False
    except:
      print "Redis connection failed, using DEBUG mode"
      DEBUG = True
      return mock
  if DEBUG:
    return mock
  else:
    return redis.Redis()
    

def get_def(name):
  name = name.lower()
  d = get_connection().hget("jargon-defs", name)
  if not d:
    return d
  return json.loads(d)

def get_all_def():
  return get_connection().hkeys("jargon-defs")

def set_def(name, defs):
  name = name.lower()
  get_connection().hdel("jargon-def-fails", name)
  return get_connection().hset("jargon-defs", name, json.dumps(defs))

def del_def(name):
  return get_connection().hdel("jargon-defs", name)

def get_failed_lookup():
  return get_connection().hgetall("jargon-def-fails")

def failed_lookup(name):
  # todo: save more info about the failed lookup
  name = name.lower()
  return get_connection().hincrby("jargon-def-fails", name, 1)

if __name__ == "__main__":
  DEBUG = True
  print get_def("nothing") == None
  set_def("test", {"test": 1})
  print get_def("test")["test"] == 1
  set_def("test", {"test": 2})
  print get_def("test")["test"] == 2
  set_def("test2", {"test": 0})
  print get_all_def()
