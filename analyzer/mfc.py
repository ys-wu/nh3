import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_mcp4725


class Mfc():

  def __init__(self, dac, adc):
    self.dac = dac
    self.dac.normalized_value = 1.0
    self.adc = adc

  def __str__(self):
    return

  

if __name__ == '__main__':
  i2c = busio.I2C(board.SCL, board.SDA)
  dac = adafruit_mcp4725.MCP4725(i2c)
  ads = ADS.ADS1015(i2c)
  adc = AnalogIn(ads, ADS.P1)

  raw_range = 4095
  mfc = Mfc(dac, adc)
  mfc.dac.raw_value = int(0.5 * raw_range)
  print(mfc.adc.voltage)
