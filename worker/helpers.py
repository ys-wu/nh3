from datetime import datetime
from time import sleep

import redis

import conf


def get_utc_time():
  return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


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


def status_setter(meassys, r):
  while r.llen('status'):
    meassys.status = r.rpop('status').decode('utf-8')


def push_to_redis(r, queue, data, limit=100):
  r.lpush(queue, data)
  while r.llen(queue) > limit:
    r.rpop(queue)


def command_handler(r, meassys):
  command_mapper = {
    'start': meassys.start,
    'stop': meassys.stop,
    'air_pump_on': meassys.air_pump_on,
    'air_pump_off': meassys.air_pump_off,
    'liquid_pump_on': meassys.liquid_pump_on,
    'liquid_pump_off': meassys.liquid_pump_off,
    'cal_gas_zero_start': meassys.cal_gas_zero_start,
    'cal_gas_zero_stop': meassys.cal_gas_zero_stop,
    'cal_liquid_span_start': meassys.cal_liquid_span_start,
    'cal_liquid_span_stop': meassys.cal_liquid_span_stop,
    'clear_error': meassys.clear_error,
    'clear_memory': meassys.clear_memory,
  }
  while r.llen('commands'):
    command = r.rpop('commands').decode('utf-8')
    command_mapper[command]()


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
