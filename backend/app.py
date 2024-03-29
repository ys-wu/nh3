from flask import Flask, request

from services import (
  get_data,
  get_error,
  send_command,
  send_status,
  send_settings,
)


app = Flask(__name__)


@app.route('/api/data')
def data():
  data = get_data()
  return data


@app.route('/api/error')
def error():
  error = get_error()
  return error


@app.route('/api/command', methods=['POST'])
def command():
  command = request.get_json()['command']
  if send_command(command):
    return {'message': 'received a command'} 
  else:
    return {'message': 'bad command'}


@app.route('/api/status', methods=['POST'])
def status():
  status = request.get_json()['status']
  if send_status(status):
    return {'message': 'received a status'}
  else:
    return {'message': 'bad status'}


@app.route('/api/settings', methods=['POST'])
def settings():
  settings = request.get_json()
  if send_settings(settings):
    return {'message': 'received settings'}
  else:
    return {'message': 'bad settings'}
