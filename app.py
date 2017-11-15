from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000, debug=True)