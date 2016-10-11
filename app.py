from flask import Flask, render_template, request, redirect
import sqlite3
import time
from subprocess import call, Popen
from readit import get_image_url, reddit_url
from log import log
INDEX_PAGE = "index.html"

app = Flask(__name__)
i = 0
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
	if request.method == 'POST':
		datetime = request.form['time']
		print(datetime)
		Popen(["python", "spotalarm", datetime])
		return redirect('/alarm')
	return render_template('alarm.html')

def print_keys(dic):
	print("Gon' print some keys")
	for key in dic:
		print("Key:")
		print(key)

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0')
