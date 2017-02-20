from flask import Flask, render_template, request, redirect, Response
import sqlite3
import time
import json
import sys
from models.Alarm import Alarm
from models.AlarmHandler import AlarmHandler
from api_gen import ApiGenerator

INDEX_PAGE = "index.html"

app = Flask(__name__, template_folder='../templates')

alarm_handler = AlarmHandler()
api_gen = ApiGenerator()

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
	Currently alarm is the main feature so we redirect there.
	"""
	return redirect('/alarm')

@app.route('/image/<img>')
def image(img):
	"""
	Image hosting
	"""
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
		read_text_as_speech(request.form['content'])
		return post_twat(request)	
	return render_template('form.html')

def post_twat(request):
	checkInput(request.form['content'])
	query = twat_to_sql_query(request)
	execute_query(query)
	return redirect("/form")

def twat_to_sql_query(request):
	return "INSERT INTO twats VALUES(\"" + request.form['content'] + "\", " + str(time.time()) + ")"

def execute_query(query, db):
	conn = sqlite3.connect('twatter.db')
	c = conn.cursor()
	c.execute(query)
	conn.commit()
	conn.close()

def read_text_as_speech(text):
	call(["flite", "-t", text])

@app.route('/alarm', methods=['GET', 'POST'])
def set_alarm():
	"""
	Creates an alarm for the time entered by the user.
	Redirects to the alarm listings page once alarm is created.
	"""
	if request.method == 'POST':
		datetime = request.form['time']
		alarm_handler.create_alarm(datetime)
		return redirect('/alarms')
	return render_template('alarm.html')

@app.route('/alarms')
def show_alarms():
	"""
	Lists all currently active alarms.
	"""
	active_alarms = alarm_handler.get_active_alarms()
	return render_template('show_alarms.html', alarms=active_alarms)

@app.route('/api/alarms')
def api_alarms():
	js = api_gen.get_alarms(alarm_handler)
	return Response(js, status=200, mimetype='application/json')
	

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
	for key in dic:
		print("Key:", key)



def main():
	if len(sys.argv) > 1:
		# Check if argument 1 enables debug mode.
		app.run(debug=(sys.argv[1] == 'debug'), host='0.0.0.0')
	else:
		app.run(debug=False, host='0.0.0.0')

if __name__ == '__main__':
	main()



