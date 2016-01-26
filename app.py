from flask import Flask, render_template

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


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')