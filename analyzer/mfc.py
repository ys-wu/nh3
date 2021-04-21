import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_mcp4725


class Mfc():

  def __init__(self, dac, adc, flow_range, raw_range=4095, volt_range=5.0):
    self.dac = dac
    self.adc = adc
    self.flow_range = flow_range
    self.raw_range = raw_range
    self.volt_range = volt_range
    self.dac.normalized_value = 1.0

  def __str__(self):
    return

  def set(self, value):
    value = value if value <= self.flow_range else self.flow_range
    self.dac.raw_value = int(self.raw_range * value / self.flow_range)
  
  @property
  def flow(self):
    return self.adc.voltage / self.volt_range * self.flow_range


if __name__ == '__main__':
  i2c = busio.I2C(board.SCL, board.SDA)
  dac = adafruit_mcp4725.MCP4725(i2c)
  ads = ADS.ADS1015(i2c)
  adc = AnalogIn(ads, ADS.P1)

  mfc = Mfc(dac, adc, 3)
  mfc.set(2)
  print(mfc.flow)
