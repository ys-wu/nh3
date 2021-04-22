from flask import Flask, request

from services import (
  get_data,
  send_command,
  send_status,
)


app = Flask(__name__)


@app.route('/data')
def data():
  data = get_data()
  return data


@app.route('/command', methods=['POST'])
def command():
  command = request.form['command']
  if send_command(command):
    return {'message': 'received a command'} 
  else:
    return {'message': 'bad command'}


@app.route('/status', methods=['POST'])
def status():
  status = request.form['status']
  if send_status(status):
    return {'message': 'received a status'}
  else:
    return {'message': 'bad status'}
