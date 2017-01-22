from flask import Flask, render_template, request, redirect, Response
import sqlite3
import time
from subprocess import call, Popen
from readit import get_image_url, reddit_url
from log import log
import json
import sys

INDEX_PAGE = "index.html"

app = Flask(__name__)
i = 0
keygen = 0
alarms = list()

class Alarm:
	"""
	A single scheduled alarm. Controls the separate alarm process.
	Does not persist between sessions so if you restart the server all alarms are lost.
	"""
	def __init__(self, key, time):
		"""
		:key - A unique identifier for this alarm. Needs only be unique for the current session.
		:time - 24-hour time string on the format HH:MM
		"""
		self.time = time
		self.key = key
		self.process = Popen(["python", "spotalarm.py", time])

	def get_process(self):
		return self.process

	def stop(self):
		"""
		Kills the process, effectively stopping the alarm from going off.
		Will not do anything once the alarm has been triggered.
		"""
		self.process.kill()

	def __str__(self):
		return str(self.time)
	
@app.route("/old")
def index_old():
	"""
	The first page of the site. Shows a random string
	from the 'twatter' system.
	"""
	conn = sqlite3.connect('twatter.db')

	c = conn.cursor()
	s = "SELECT * FROM twats ORDER BY RANDOM() LIMIT 1"
	c.execute(s)
	data = c.fetchone()
	conn.close()
	message = data[0]
	
	return render_template(INDEX_PAGE, message=message)

def checkInput(s):
	"""
	Checks the validity of s. Currently only
	if the string is non-empty.
	"""
	print("bout to raise")
	if len(s) == 0:
		print("raised")
		raise Exception("Nonono")
	
@app.route('/')
def index():
	"""
	Shows cat pictures.
	"""
	log(request)
	url = get_image_url(reddit_url, cache=True)
	return render_template('remote_image.html', url=url)


@app.route('/image/<img>')
def image(img):
	"""
	Some basic image hosting.
	"""
	print(img)
	return render_template('image.html', img=img)



@app.route('/form', methods=['GET', 'POST'])
def twatter_form():
	"""
	Twatter. Takes a string from the user and
	plays it on my speaker using text to speech.
	Also permanently stores the string for usage
	on the old main page.
	"""
	if request.method == 'POST':
		
		conn = sqlite3.connect('twatter.db')
		c = conn.cursor()
		checkInput(request.form['content'])

		# TODO: See if I can pull off some SQL injection on this
		s = "INSERT INTO twats VALUES(\"" + request.form['content'] + "\", " + str(time.time()) + ")"
		
		c.execute(s)
		conn.commit()
		conn.close()

		# Text to speech
		call(["flite", "-t", request.form['content']])

		return redirect("/form")
	return render_template('form.html')

@app.route('/alarm', methods=['GET', 'POST'])
def set_alarm():
	"""
	Creates an alarm for the time entered by the user.
	Redirects to the alarm listings page once alarm is created.
	"""
	global alarms
	global keygen
	if request.method == 'POST':
		datetime = request.form['time']
		print(datetime)
		
		alarms.append(Alarm(keygen, datetime))
		keygen += 1
		return redirect('/alarms')
	return render_template('alarm.html')

@app.route('/alarms')
def show_alarms():
	"""
	Lists all currently active alarms.
	"""
	global alarms
	for alarm in alarms:
		alarm.get_process().poll()
		if alarm.get_process().returncode != None:
			alarms.remove(alarm)
	return render_template('show_alarms.html', alarms=alarms)

@app.route('/api/alarms')
def api_alarms():
	"""
	Returns a json object with alarm time of all active alarms.
	"""
	data = {}
	for i, alarm in enumerate(alarms):
		data[str(alarm.key)] = str(alarm.time)
	js = json.dumps(data)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route('/api/alarms/remove/<key>', methods=['POST'])
def api_remove(key, action):
	"""
	API functionality to remove the alarm given by key.
	If no alarm matches key nothing happens but the user is not notified.
	Returns a json object just containing the key.
	"""
	global alarms
	key = int(key)

	for i, alarm in enumerate(alarms):
		if alarm.key == key:
			alarm.stop()
			del alarms[i]
			i -= 1
			if not alarms:
				alarms = list()
	data = {'key': str(key)}
	js = json.dumps(data)

	# TODO: Better response. Shouldn't be 200 every time.
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route('/api/alarms/create/<time>', methods=['POST'])
def api_create(time):
	"""
	API functionality for creating an alarm.
	Returns a json object with the key and time for
	the new alarm.
	"""
	global alarms
	global keygen
	datetime = time[:2] + ':' + time[2:]
	
	print(datetime)
	
	alarms.append(Alarm(keygen, datetime))
	keygen += 1
	data = {'key': str(key), 'time': datetime}
	js = json.dumps(data)
	resp = Response(js, status=200, mimetype='application/json')
	return resp


def print_keys(dic):
	"""
	Does what it says it does.
	"""
	print("Gon' print me some keys")
	for key in dic:
		print("Key:", key)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		# Check if argument 1 enables debug mode.
		app.run(debug=(sys.argv[1] == 'debug'), host='0.0.0.0')
	else:
		app.run(debug=False, host='0.0.0.0')



