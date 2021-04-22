from flask import Flask, request

from services import (
  get_data,
)


app = Flask(__name__)


@app.route('/data')
def hello_world():
  data = get_data()
  return data
