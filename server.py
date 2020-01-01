import os
import sys
import json
from http import client
from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def post():


# Start app
port = 5000
host = 'localhost'
if 'PORT' in os.environ:
	port = os.environ['PORT']
	host = '0.0.0.0'
app.run(host = host, port = port)
