from time import sleep

import redis

import conf


r = redis.Redis(
  host=conf.REDIS['HOST'],
  port=conf.REDIS['PORT'],
  db=conf.REDIS['DB'],
)

# commands = [
#   'stop',
#   'start',
#   'air_pump_off',
#   'air_pump_on',
#   'liquid_pump_off',
#   'liquid_pump_on',
#   'cal_gas_zero_start',
#   'cal_gas_zero_stop',
#   'cal_liquid_span_start',
#   'cal_liquid_span_stop',
#   'clear_error',
#   'clear_memory',
#   'stop',
# ]

# for command in commands:
#   sleep(5)
#   print(command)
#   r.lpush('commands', command)

# for status in ['x','y', 'z', 'Sampling']:
#   sleep(5)
#   print(status)
#   r.lpush('status', status)


while True:
  sleep(1)
  # while r.llen('data') > 1:
  #   r.rpop('data')
  if r.llen('data') > 0:
    print(r.rpop('data').decode('utf-8'))
