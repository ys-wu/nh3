from datetime import datetime
from time import sleep
from configparser import ConfigParser
import json

import redis

import conf


def clear_up_redis(r):
  while r.llen('data'):
    r.rpop('data')
  while r.llen('commands'):
    r.rpop('commands')
  while r.llen('status'):
    r.rpop('status')
  while r.llen('errors'):
    r.rpop('errors')
  while r.llen('settings'):
    r.rpop('settings')


config = ConfigParser()
config.read('settings.ini')
SETTINGS = {
  'AUTO_START':
    True if config['SETTINGS']['AUTO_START'].lower() == 'true' else False,
  'AUTO_PUBLISH':
    True if config['SETTINGS']['AUTO_PUBLISH'].lower() == 'true' else False,
  'AUTO_BACKUP':
    True if config['SETTINGS']['AUTO_BACKUP'].lower() == 'true' else False,
  'LOCAL_PUBLISH_INTERVAL':
    int(config['SETTINGS']['LOCAL_PUBLISH_INTERVAL']),
  'LOCAL_RECORD_INTERVAL':
    int(config['SETTINGS']['LOCAL_RECORD_INTERVAL']),
  'REMOTE_PUBLISH_INTERVAL':
    int(config['SETTINGS']['REMOTE_PUBLISH_INTERVAL']),
  'REMOTE_BACKUP_INTERVAL':
    int(config['SETTINGS']['REMOTE_BACKUP_INTERVAL']),
}

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

GENS = {
  'local_pub': is_new_start(SETTINGS['LOCAL_PUBLISH_INTERVAL']),
  'local_record': is_new_start(SETTINGS['LOCAL_RECORD_INTERVAL']),
  'remote_pub': is_new_start(SETTINGS['REMOTE_PUBLISH_INTERVAL']),
  'remote_backup': is_new_start(SETTINGS['REMOTE_BACKUP_INTERVAL']),
}

def setting_handler(r):
  while r.llen('settings'):
    for key, value in json.loads(r.rpop('settings')).items():
      if key == 'auto_start':
        config.set('SETTINGS', 'AUTO_START', str(value))
      elif key == 'auto_publish':
        config.set('SETTINGS', 'AUTO_PUBLISH', str(value))
      elif key == 'auto_backup':
        config.set('SETTINGS', 'AUTO_BACKUP', str(value))
      elif key == 'local_publish_interval':
        config.set('SETTINGS', 'LOCAL_PUBLISH_INTERVAL', str(value))
        GENS['local_pub'] = is_new_start(value)
      elif key == 'local_record_interval':
        config.set('SETTINGS', 'LOCAL_RECORD_INTERVAL', str(value))
        GENS['local_record'] = is_new_start(value)
      elif key == 'remote_publish_interval':
        config.set('SETTINGS', 'REMOTE_PUBLISH_INTERVAL', str(value))
        GENS['remote_publish'] = is_new_start(value)
      elif key == 'remote_backup_interval':
        config.set('SETTINGS', 'REMOTE_BACKUP_INTERVAL', str(value))
        GENS['remote_backup'] = is_new_start(value)
    with open('settings.ini', 'w') as configfile:
      config.write(configfile)


def get_utc_time():
  return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


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

  # for i in range(10):
  #   push_to_redis(r, 'data', i, 5)
  # while r.llen('data'):
  #   print(r.rpop('data'))

  settings = [
    {'auto_start': False, 'local_publish_interval': 2},
    {'remote_backup_interval': 3600},
    {'auto_publish': False, 'auto_backup': False, 'local_record_interval':10},
    {'remote_publish_interval': 60}
  ]
  for x in settings:
    r.lpush('settings', json.dumps(x))
  setting_handler(r)
