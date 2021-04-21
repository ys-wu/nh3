from datetime import datetime
from time import sleep



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


if __name__ == '__main__':

  gen = is_new_start(2)
  for i in range(10):
    sleep(0.5)
    print(datetime.now(), next(gen))

  print('*' * 20)

  gen = is_new_start(5)
  for i in range(20):
    sleep(0.5)
    print(datetime.now(), next(gen))
