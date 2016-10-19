from flask import Flask, render_template, request, redirect
import sqlite3
import time
from subprocess import call, Popen
from readit import get_image_url, reddit_url
from log import log
INDEX_PAGE = "index.html"

app = Flask(__name__)
i = 0
alarms = list()

class Alarm:
	def __init__(self, time):
		self.time = time
		self.process = Popen(["python", "spotalarm.py", time])

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
	if request.method == 'POST':
		datetime = request.form['time']
		print(datetime)
		alarms.append(Alarm(datetime))
		return redirect('/alarms')
	return render_template('alarm.html')

@app.route('/alarms')
def show_alarms():
	global alarms
	return render_template('show_alarms.html', alarms=alarms)

def print_keys(dic):
	print("Gon' print some keys")
	for key in dic:
		print("Key:")
		print(key)

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0')



