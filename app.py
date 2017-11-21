from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import requests
import sys
import bs4
import RandomHeaders
import re

app = Flask(__name__)

def returnProxies(csvpath):
	with open(csvpath, 'rb') as f:
		reader = csv.reader(f)
		return list(reader)

def getCommits():
	try:
		url = 'https://github.com/theriley106/SneakerBotTutorials'
		res = requests.get(url, headers=RandomHeaders.LoadHeader())
		page = bs4.BeautifulSoup(res.text)
		commitsCount = page.select('.commits a')
		return int(re.findall('\d+', str(commitsCount[0].getText()))[0])
	except:
		return "ERROR"


@app.route('/', methods=['GET'])
def index():
	gitCommits = getCommits()
	return render_template("index.html", gitCommits=gitCommits)



if __name__ == '__main__':
	PROXIES = []
	if len(sys.argv) > 1:
		if '.csv' in str(sys.argv[1]):
			PROXIES = returnProxies(sys.argv[1])
		if len(sys.argv) > 1 and '.csv' not in str(sys.argv[1]):
			for proxy in sys.argv[1:]:
				PROXIES.append(proxy)
		for proxy in PROXIES:
			print("Initiating Bot with Proxy: {}".format(proxy))
	app.run(host='127.0.0.1', port=8000, debug=True)