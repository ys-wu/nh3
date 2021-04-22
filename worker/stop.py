from time import sleep

import redis

import conf

from helpers import get_utc_time


r = redis.Redis(
  host=conf.REDIS['HOST'],
  port=conf.REDIS['PORT'],
  db=conf.REDIS['DB'],
)
r.lpush('commands', 'stop')
print(get_utc_time(), 'send stop command to redis')
