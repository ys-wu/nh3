from time import sleep

import conf

from airrmonia import Airrmonia
# from mfc import Mfc


class MeasSys():

  def __init__(self, airrmonia, mfc_sample=None, mfc_cal=None):
    self.airrmonia = airrmonia
    # self.mfc_sample = mfc_sample
    # self.mfc_cal = mfc_cal
    self.status = 'Idle'

  def __str__(self):
    return 'Airrmonia + Sample MFC + Calibration MFC'
  
  def start(self):
    # self.mfc_cal.set(0)
    self.airrmonia.start()
    # self.mfc_sample.set(conf.MFC_SAMPLE['FLOW'])
    self.status = 'Sampling'

  def stop(self):
    # self.mfc_cal.set(0)
    self.airrmonia.stop()
    # self.mfc_sample.set(0)
    self.status = 'Idle'

  def air_pump_on(self):
    self.airrmonia.air_pump_on()

  def air_pump_off(self):
    self.airrmonia.air_pump_off()

  def liquid_pump_on(self):
    self.airrmonia.liquid_pump_on()

  def liquid_pump_off(self):
    self.airrmonia.liquid_pump_off()

  # def cal_gas_zero_start(self):
  #   self.mfc_cal.set(conf.MFC_CAL['FLOW'])
  #   if not self.status == 'Servicing':
  #     self.status = 'GasZero'

  # def cal_gas_zero_stop(self):
  #   self.mfc_cal.set(0)
  #   if not self.status == 'Servicing':
  #     self.status = 'Sampling'

  def cal_liquid_span_start(self):
    self.air_pump_off()
    sleep(1)
    self.airrmonia.liquid_span_cal_valve_on()
    if not self.status.startswith('Servicing'):
      self.status == ('Servicing')
    else:
      self.status = 'LiqSpan'

  def cal_liquid_span_stop(self):
    self.airrmonia.liquid_span_cal_valve_off()
    sleep(1)
    self.air_pump_on()
    if not self.status.startswith('Servicing'):
      self.status == ('Servicing')
    else:
      self.status = 'Sampling'
  
  def clear_error(self):
    self.airrmonia.clear_error()
  
  def clear_memory(self):
    self.airrmonia.clear_memory()

  @property
  def data(self):
    data = self.airrmonia.data
    
    if data is None:
      return None
  
    data, status = data
    data['Status'] = self.status
    # data['AirFlow'] = self.mfc_sample.flow
    # data['ZeroFlow'] = self.mfc_cal.flow
    errors = []

    # if data['AirFlow'] < conf.MFC_SAMPLE['LOWER_LIMIT']:
    #   data['NH3'] = None
    #   errors.append('LowSampleFlow')
    # elif data['AirFlow'] > conf.MFC_SAMPLE['UPPER_LIMIT']:
    #   data['NH3'] = None
    #   errors.append('HighSampleFlow')
    # else:
    #   data['NH3'] = int(data['NH4'] * conf.COEF / data['AirFlow'])

    return data, status, errors


if __name__ == '__main__':

  airrmonia = Airrmonia(conf.PORT)

  mfc_sample = Mfc(
    conf.MFC_SAMPLE['NAME'],
    conf.MFC_SAMPLE['DAC'],
    conf.MFC_SAMPLE['ADC'],
    conf.MFC_SAMPLE['RANGE']
  )

  mfc_cal = Mfc(
    conf.MFC_CAL['NAME'],
    conf.MFC_CAL['DAC'],
    conf.MFC_CAL['ADC'],
    conf.MFC_CAL['RANGE']
  )

  meassys = MeasSys(airrmonia, mfc_sample, mfc_cal)
  print(meassys)
  meassys.start()

  for i in range(10):
    sleep(1)
    print(meassys.data)

  meassys.stop()
  sleep(1)
  print(meassys.data) 
