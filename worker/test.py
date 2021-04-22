import time
import redis

import conf


r = redis.Redis(
  host=conf.REDIS['HOST'],
  port=conf.REDIS['PORT'],
  db=conf.REDIS['DB'],
)

commands = [
  'stop',
  'start',
  'air_pump_off',
  'air_pump_on',
  'liquid_pump_off',
  'liquid_pump_on',
  'cal_gas_zero_start',
  'cal_gas_zero_stop',
  'cal_liquid_span_start',
  'cal_liquid_span_stop',
  'clear_error',
  'clear_memory',
  'stop',
]

for command in commands:
  time.sleep(5)
  print(command)
  r.lpush('commands', command)
