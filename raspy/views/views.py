from flask import Flask, render_template, request, redirect, Response, send_from_directory
import sqlite3
import time
import json
import sys
from raspy.models.Alarm import Alarm
from raspy.models.AlarmHandler import AlarmHandler
from raspy.models.api_gen import AlarmApiGenerator
from raspy import app, api_gen, alarm_handler, light_controller, mpd_controller
from subprocess import call

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

@app.route('/api/play', methods=['POST'])
def api_play():
	resp = api_gen.play()
	return resp

@app.route('/api/pause', methods=['POST'])
def api_pause():
	resp = api_gen.pause()
	return resp

@app.route('/light/on', methods=['POST'])
def light_on():
	code = light_controller.light_on()
	data = {'code': code}
	js = json.dumps(data)
	return Response(js, status=200, mimetype='application/json')

@app.route('/light/off', methods=['POST'])
def light_off():
	code = light_controller.light_off()
	data = {'code': code}
	js = json.dumps(data)
	return Response(js, status=200, mimetype='application/json')

@app.route('/api/next', methods=['POST'])
def next_song():
	resp = api_gen.next_song()
	return resp

@app.route('/api/prev')
def prev_song():
	resp = api_gen.prev_song()
	return resp

@app.route('/robots.txt')
def robots():
	return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/playlists')
def playlists():
	plists = mpd_controller.get_playlists()
	return render_template('playlists.html', playlists=plists)

@app.route('/panel', methods=['GET', 'POST'])
def panel():
	print(request.method)
	if request.method == 'POST':
		print(request.form['submit'])
		if request.form['submit'] == 'Play':
			api_gen.play()
		elif request.form['submit'] == 'Pause':
			api_gen.pause()
		elif request.form['submit'] == 'LightOn':
			light_controller.light_on()
		elif request.form['submit'] == 'LightOff':
			light_controller.light_off()
		
	return render_template('control_panel.html')


def main():
	if len(sys.argv) > 1:
		# Check if argument 1 enables debug mode.
		app.run(debug=(sys.argv[1] == 'debug'), host='0.0.0.0')
	else:
		app.run(debug=False, host='0.0.0.0')

if __name__ == '__main__':
	main()



