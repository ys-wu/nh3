import time
import re

import conf


class Airrmonia():

  def __init__(self, port):
    self.ser = port

  def __str__(self):
    return f'Port: {self.ser}.' if self.ser else f'Not connected.'

  def _parse_status(self, status_hex):
    code = bin(int(status_hex, 16))[2:].zfill(9)[::-1]
    status = {}
    for key, value in conf.STATUS_BITS.items():
        status[key] = int(code[value])
    return status

  def _parse_data(self, string):
    sep = conf.CHARS['CR'] + conf.CHARS['LF']
    str_arr = string.split(sep)
    str_arr = str_arr[0:-1]  # delete last element (empty or incomplete)
    columns = ['Status', 'Temperature', 'AirFlow','Detector1', 'Detector2', 'Conductivity', 'NH4', 'NH3']
    pattern = 'Y;\d{5}.\d{5};\d{2};\d{1};\d{2};[a-zA-Z0-9]{4};\d{4};\d{3};\d{5};\d{5};.\d{4};.\d{4,5};.\d{4,5}'
    for s in str_arr:
      if s and s[0] == conf.COMMANDS['Data'] and re.fullmatch(pattern, s):
        x = s.split(';')
    if 'x' in locals():
      data = [x[5], int(x[6])/100, int(x[7])/100, int(x[8])/10, int(x[9])/10, int(x[10])/10, int(x[11])/10, int(x[12])/100]
      data = dict(zip(columns, data))
      status = self._parse_status(data['Status'])
      return [data, status]
    else:
      return None

  @property
  def data(self):
    r = self.ser.read(10000).decode('utf-8')
    if r:
      return self._parse_data(r)
    else:
      return None

  def _send_command(self, command, param=None):
    if param:
      s = conf.CHARS['STX'] + command + param + CHARS['CR']
    else:
      s = conf.CHARS['Esc'] + command
    self.ser.write(s.encode('utf-8'))

  def start(self):
    self._send_command(conf.COMMANDS['Start'])

  def stop(self):
    self._send_command(conf.COMMANDS['Stop'])

  def air_pump_on(self):
    self._send_command(conf.COMMANDS['AirPump'], 1)

  def air_pump_off(self):
    self._send_command(conf.COMMANDS['AirPump'], 0)

  def liquid_pump_on(self):
    self._send_command(conf.COMMANDS['LiqPump'], 1)

  def liquid_pump_off(self):
    self._send_command(conf.COMMANDS['LiqPump'], 0)

  def liquid_span_cal_valve_on(self):
    self._send_command(conf.COMMANDS['SetValve'], 1)

  def liquid_span_cal_valve_off(self):
    self._send_command(conf.COMMANDS['SetValve'], 0)

  def clear_error(self):
    self._send_command(conf.COMMANDS['Error'])

  def clear_memory(self):
    self._send_command(conf.COMMANDS['Mem'])


if __name__ == '__main__':
  inst = Airrmonia(conf.PORT)
  inst.start()
  for i in range(10):
    time.sleep(1)
    print(inst.data)
  inst.stop()
  time.sleep(1)
  print(inst.data)
