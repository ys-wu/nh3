CAL = {0: 0, 50: 381.6, 500: 1381.5}  # 2018.06 calibration
COEF = 26  # liquid NH4+ (ppbm) to gas NH3 (pptv)
INTERVAL = 5  # samnpling time invteval

COMMANDS = {
  'Status': '?',
  'Mode': 'M',
  'Start': 'E',
  'Stop': 'S',
  'Error': '!',
  'Mem': 'C',
  'Reset': 'R',
  'Data': 'Y',
  'AirPump': 'A',
  'LiqPump': 'Q',
  'Valve': 'V',
  'Fan': 'F'
}

CHARS = {
  'STX': '\x02',
  'LF': '\x0a',
  'CR': '\x0d',
  'Esc': '\x1b'
}

STATUS_BITS = {
  'AirPump': 0,
  'LiqPump': 1,
  'Fan': 2,
  'Heater': 3,
  'AutoStart': 4,
  'ErrorFlag': 5,
  'Bottle': 6,
  'DataMemory': 7,
  'CalMemory': 8
}
