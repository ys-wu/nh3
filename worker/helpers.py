from datetime import datetime
from time import sleep

import redis

import conf


def is_new_start(interval):

  # check whole seconds
  t0 = int(datetime.now().timestamp())

  while True:
    t1 = int(datetime.now().timestamp())
    if (t1 > t0) and (t1 % interval == 0):
      yield True
      t0 = t1
    else:
      yield False


def push_to_redis(r, queue, data, limit=100):
  r.lpush(queue, data)
  while r.llen(queue) > limit:
    r.rpop(queue)


if __name__ == '__main__':

  # gen = is_new_start(2)
  # for i in range(10):
  #   sleep(0.5)
  #   print(datetime.now(), next(gen))

  # print('*' * 20)

  # gen = is_new_start(5)
  # for i in range(20):
  #   sleep(0.5)
  #   print(datetime.now(), next(gen))

  r = redis.Redis(
    host=conf.REDIS['HOST'],
    port=conf.REDIS['PORT'],
    db=conf.REDIS['DB'],
  )

  for i in range(10):
    push_to_redis(r, 'data', i, 5)
  while r.llen('data'):
    print(r.rpop('data'))
