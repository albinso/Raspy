from flask import Flask, render_template, request, redirect, Response
import sqlite3
import time
import json
import sys
from raspy.models.Alarm import Alarm
from raspy.models.AlarmHandler import AlarmHandler
from raspy.models.api_gen import AlarmApiGenerator
from raspy import app, api_gen, alarm_handler

INDEX_PAGE = "index.html"
	
@app.route('/')
def index():
	"""
	Currently alarm is the main feature so we redirect there.
	"""
	return redirect('/alarm')

@app.route('/image/<img>')
def image(img):
	"""
	Image hosting
	"""
	return render_template('image.html', img=img)

@app.route('/alarm', methods=['GET', 'POST'])
def set_alarm():
	"""
	Redirects to the alarm listings page once alarm is created.
	"""
	if request.method == 'POST':
		datetime = request.form['time']
		alarm_handler.create_alarm(datetime)
		return redirect('/alarms')
	return render_template('alarm.html')

@app.route('/alarms')
def show_alarms():
	active_alarms = alarm_handler.get_active_alarms()
	return render_template('show_alarms.html', alarms=active_alarms)

@app.route('/api/alarms')
def api_alarms():
	resp = api_gen.get_alarms_response()
	return resp
	

@app.route('/api/alarms/remove/<key>', methods=['POST', 'GET'])
def api_remove_alarm(key):
	key = int(key)
	resp = api_gen.remove_alarm_by_key(key)	
	return resp

@app.route('/api/alarms/create/<time>', methods=['POST', 'GET'])
def api_create(time):
	"""
	API functionality for creating an alarm.
	Returns a json object with the key and time for
	the new alarm.
	"""
	alarm_time = time[:2] + ':' + time[2:]
	resp = api_gen.create_alarm(alarm_time)
	return resp

@app.route('/api/volume/set/<vol>')
def api_set_volume(vol):
	resp = api_gen.set_volume(vol)
	return resp


def main():
	if len(sys.argv) > 1:
		# Check if argument 1 enables debug mode.
		app.run(debug=(sys.argv[1] == 'debug'), host='0.0.0.0')
	else:
		app.run(debug=False, host='0.0.0.0')

if __name__ == '__main__':
	main()



