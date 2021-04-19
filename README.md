# Ammonia-analyzer

## Dev Tools

### remote.it access to Raspberry Pi
- `remote.it`

### VSCode Remote-SSH
- `Cmd+Shift-P`
- `Remote-SSH: Open SSH Configuration file...`
- `Remote-SSH: Connect to Host...`

### Markdown 
- `sudo apt-get install pandoc lynx`
- `pandoc README.md | lynx -stdin`

## Communication
- `RS232, baudrate=19200`
- `Raw data format: b'Y;JJJJJ.jjjjj;PP;M;CC;EEEE;TTTT;fff;sssss;SSSSS;-tttt;-0NH4;-0NH3<cr><lf>'`
  - Y: Start of String
  - JJJJJ.jjjjj: Time and date in 1900 format (Excel format)
  - M: status bit (1=Measure, 2=calibration)
  - CC: Calibration number (00 till 99)
  - EEEE: Status bit
  - fff: airflow
  - sssss: mV of Detector 1
  - SSSSS: mV of Detector 2
  - tttt: temperature correct conductivity
  - 0NH4: calculated NH4 (ppB / 10)
  - 0NH3: calculated NH3 (ug/m3 / 100)
- `Raw data example: b'Y;44305.49296;60;1;01;000F;2256;098;03040;02796;-0226;-0011;-0023\r\n'`

## Python
- `python3 --version` 3.7.3
- `python3 -m venv venv`
- `source venv/bin/activate`
