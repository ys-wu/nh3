# Ammonia-analyzer

## Dev Tools

### Remote access to Raspberry Pi
- `remote.it`
- frp
- `scp -P <port number> -r local/path user@hostname:destination/path/`

### VSCode Remote-SSH
- `Cmd+Shift-P`
- `Remote-SSH: Open SSH Configuration file...`
- `Remote-SSH: Connect to Host...`

### Markdown 
- `sudo apt-get install pandoc lynx`
- `pandoc README.md | lynx -stdin`

### Useful commands
- `sudo cat /proc/cpuinfo`
- `getconf LONG_BIT`
- `sudo ufw allow <port number>`
- `sudo nestat -npl | grep vnc`

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

### VScode config
- pylance
```
{
  "python.pythonPath": "venv/bin/python3",
  "python.analysis.extraPaths": [
    "./worker",
    "./backend",
  ],
}
```

## Redis
- `sudo apt-get update`
- `sudo apt-get install redis-server`

## React
- `sudo apt-get install nodejs npm`
- `sudo npm install -g npx`
- `sudo yarn add antd --network-timeout 100000`

## Nginx
- `sudo apt install nginx`
- `sudo /etc/init.d/nginx start`
- `cat /etc/nginx/sites-enabled/default`
- `sudo cp nginx/default /etc/nginx/sites-enabled/`
- `sudo /etc/init.d/nginx restart`

## MongoDB
- `sudo apt update`
- `sudo apt upgrade`
- `sudo apt install mongodb`
- `sudo systemctl enable mongodb`
- `sudo systemctl start mongodb`
- `mongod --version`
- shell `mongo`
  - `show dbs`
  - `use <db>`
  - `db.dropDatabase()`
  - `db.data.find().sort({ $natural: -1}).limit(1)`
