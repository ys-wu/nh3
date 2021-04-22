REDIS = {
    'HOST': 'localhost',
    'PORT': 6379,
    'DB': 0,
}

COMMANDS = [
    'start',
    'stop',
    'air_pump_on',
    'air_pump_off',
    'liquid_pump_on',
    'liquid_pump_off',
    'cal_gas_zero_start',
    'cal_gas_zero_stop',
    'cal_liquid_span_start',
    'cal_liquid_span_stop',
    'clear_error',
    'clear_memory',
]

STATUS = [
    'Idle',
    'Sampling',
    'GasZero',
    'LiqSpan',
    'Servicing',
]

SETTINGS = [
    'auto_start',
    'auto_publish',
    'auto_backup',
    'local_publish_interval',
    'local_record_interval',
    'remote_publish_interval',
    'remote_backup_interval',
]
