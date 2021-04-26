from time import sleep
# import json

# import redis
from pymongo import MongoClient, DESCENDING

# import conf


MONGODB = {
  'HOST': 'localhost',
  'PORT': 27017,
  'DB': 'nh3',
  'COL': 'data',
}
db = MongoClient(MONGODB['HOST'], MONGODB['PORT'])[MONGODB['DB']]
collection = db[MONGODB['COL']]
for i in range(10):
  sleep(11)
  print(collection.find_one(sort=[('_id', DESCENDING)]))

# r = redis.Redis(
#   host=conf.REDIS['HOST'],
#   port=conf.REDIS['PORT'],
#   db=conf.REDIS['DB'],
# )

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
 
# for i in range(30):
#   sleep(0.5)
#   while r.llen('data') > 1:
#     r.rpop('data')
#   if r.llen('data') > 0:
#     print(r.rpop('data').decode('utf-8'))

# r.lpush('settings', json.dumps({'local_publish_interval': 1}))

# for i in range(30):
#   sleep(0.5)
#   while r.llen('data') > 1:
#     r.rpop('data')
#   if r.llen('data') > 0:
#     print(r.rpop('data').decode('utf-8'))

# r.lpush('settings', json.dumps({'local_publish_interval': 2}))

# while True:
#   sleep(1)
#   while r.llen('data') > 1:
#     r.rpop('data')
#   if r.llen('data') > 0:
#     print(r.rpop('data').decode('utf-8'))
