import json

import redis

import conf


r = redis.Redis(
  host=conf.REDIS['HOST'],
  port=conf.REDIS['PORT'],
  db=conf.REDIS['DB'],
)


def get_data():
  if r.llen('data') > 0:
    data = r.lpop('data')
    while r.llen('data') > 0:
      r.rpop('data')
    return json.loads(data)
  else:
    return {'data': None}


def send_command(command):
  if command in conf.COMMANDS:
    r.lpush('commands', command)
    return True
  else:
    return False


def send_status(status):
  if status in conf.STATUS:
    r.lpush('status', status)
    return True
  else:
    return False
