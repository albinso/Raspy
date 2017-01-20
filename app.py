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
	def __init__(self, key, time):
		self.time = time
		self.key = key
		self.process = Popen(["python", "spotalarm.py", time])

	def get_process(self):
		return self.process

	def stop(self):
		self.process.kill()

	def __str__(self):
		return str(self.time)
	
@app.route("/old")
def index_old():
	conn = sqlite3.connect('twatter.db')

	c = conn.cursor()
	s = "SELECT * FROM twats ORDER BY RANDOM() LIMIT 1"
	c.execute(s)
	data = c.fetchone()
	conn.close()
	message = data[0]
	
	return render_template(INDEX_PAGE, message=message)

def checkInput(s):
	print("bout to raise")
	if len(s) == 0:
		print("raised")
		raise Exception("Nonono")
	
@app.route('/')
def index():
	log(request)
	url = get_image_url(reddit_url, cache=True)
	return render_template('remote_image.html', url=url)

@app.route('/user/')
def no_user():
	return user("")
@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)
@app.route('/image/<img>')
def image(img):
	print(img)
	return render_template('image.html', img=img)



@app.route('/form', methods=['GET', 'POST'])
def handle_data():
	if request.method == 'POST':
		
		conn = sqlite3.connect('twatter.db')

		c = conn.cursor()
		checkInput(request.form['content'])
		s = "INSERT INTO twats VALUES(\"" + request.form['content'] + "\", " + str(time.time()) + ")"
		
		c.execute(s)
		conn.commit()
		conn.close()
		call(["flite", "-t", request.form['content']])
		return redirect("/form")
	return render_template('form.html')

@app.route('/alarm', methods=['GET', 'POST'])
def set_alarm():
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
	global alarms
	for alarm in alarms:
		alarm.get_process().poll()
		if alarm.get_process().returncode != None:
			alarms.remove(alarm)
	return render_template('show_alarms.html', alarms=alarms)

@app.route('/api/alarms')
def api_alarms():
	data = {}
	for i, alarm in enumerate(alarms):
		data[str(alarm.key)] = str(alarm.time)
	js = json.dumps(data)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route('/api/alarms/act/<key>/<action>')
def api_act(key, action):
	key = int(key)

	if action == 'remove':
		for i, alarm in enumerate(alarms):
			if alarm.key == key:
				alarm.stop()
				del alarms[i]
	data = {'key': str(key)}
	js = json.dumps(data)
	resp = Response(js, status=200, mimetype='application/json')
	return resp


def print_keys(dic):
	print("Gon' print some keys")
	for key in dic:
		print("Key:")
		print(key)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		app.run(debug=(sys.argv[1] == 'true'), host='0.0.0.0')
	else:
		app.run(debug=False, host='0.0.0.0')



