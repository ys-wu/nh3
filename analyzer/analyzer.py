import glob
import time
import serial

import conf


class Instrument():

  def __init__(self, baudrate=19200, timeout=0.5):
    self.baudrate = baudrate
    self.timeout = timeout

  def __str__(self):
    return f'Port: {self.port}.' if self.port else f'Not connected.'

  def check_port(self):
    ports = glob.glob('/dev/ttyUSB*')
    for p in ports:
      ser = serial.Serial(p)
      ser.baudrate = self.baudrate
      ser.timeout = self.timeout
      time.sleep(2)
      while True:
        s = ser.read(1000)
        if s:
          while True:
            s = ser.read(1000)
            if s:
              self.port = p
              return
  
  def init_port(self):
    self.check_port()
    ser = serial.Serial(self.port)
    ser.baudrate = self.baudrate
    ser.timeout = self.timeout
    self.ser = ser
  
  def _send_command(self, command, param=None, method='get'):
    if method == 'get':
        s = CHARS['Esc'] + command
    elif method == 'set':
        s = CHARS['STX'] + command + param + CHARS['CR']
    cmd = s.encode('utf-8')
    self.ser.write(cmd)

  def _parse_data(self, string):
    if isinstance(string, bytes):
      try:
        string = string.decode('utf-8')
      except UnicodeDecodeError:
        return None
    sep = self.conf.CHARS['CR'] + self.conf.CHARS['LF']
    str_arr = string.split(sep)
    str_arr = str_arr[0:-1]  # delete last element (empty or incomplete)
    print(str_arr)
    columns = ['Status', 'temperature', 'airflow','Detector1', 'Detector2', 'conductivity', 'NH4', 'NH3']
    pattern = 'Y;\d{5}.\d{5};\d{2};\d{1};\d{2};[a-zA-Z0-9]{4};\d{4};\d{3};\d{5};\d{5};.\d{4};.\d{4,5};.\d{4,5}'
    for s in str_arr:
      if s and s[0] == self.conf.COMMANDS['Data'] and re.fullmatch(pattern, s):
        x = s.split(';')
    if 'x' in locals():
      data = [x[5], int(x[6])/100, int(x[7])/100, int(x[8])/10, int(x[9])/10, int(x[10])/10, int(x[11])/10, int(x[12])/100]
      return dict(zip(columns, data))
    else:
      return None
  
  @property
  def data(self):
    r = self.ser.read(10000)
    if r:
      return self._parse_data(r)
    else:
      return None


if __name__ == '__main__':
  inst = Instrument()
  inst.init_port()
  print(inst)
