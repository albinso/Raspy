from flask import Flask, render_template, request, redirect
import sqlite3
import time

INDEX_PAGE = "index.html"

app = Flask(__name__)
i = 0
@app.route('/')
def index():
	global i
	i+=1
	if i == 3:
		i = 0
		return "Today's special!"
	return render_template(INDEX_PAGE)

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
		print(request.form.keys())
		s = "INSERT INTO twats VALUES(\"" + request.form['content'] + "\", " + str(time.time()) + ")"
		print(s)
		c.execute(s)
		print("got this far")
		conn.commit()
		conn.close()
		return redirect("/form")
	return render_template('form.html')

def print_keys(dic):
	print("Gon' print some keys")
	for key in dic:
		print("Key:")
		print(key)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')