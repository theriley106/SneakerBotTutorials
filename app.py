from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import requests
import sys
import bs4
import RandomHeaders
import re
import urllib
import time
from time import gmtime, strftime

app = Flask(__name__)

def getPing(url):
	#If someone could make a better implementation of this that would be awesome
	nf = urllib.urlopen(url)
	start = time.time()
	page = nf.read()
	end = time.time()
	nf.close()
	return format((end - start), '.5f')

def returnTime():
	#I know this doesn't adjust for local time - will fix this soon
	return strftime("%H:%M:%S", gmtime())


def returnProxies(csvpath):
	with open(csvpath, 'rb') as f:
		reader = csv.reader(f)
		return list(reader)

def getCommits():
	try:
		url = 'https://github.com/theriley106/SneakerBotTutorials'
		res = requests.get(url, headers=RandomHeaders.LoadHeader())
		page = bs4.BeautifulSoup(res.text, 'lxml')
		commitsCount = page.select('.commits a')
		return int(re.findall('\d+', str(commitsCount[0].getText()))[0])
	except:
		return "ERROR"


@app.route('/', methods=['GET'])
def index():
	gitCommits = getCommits()
	info = []
	if len(PROXIES) > 0:
		for proxy in PROXIES:
			try:
				proxyInfo = {}
				proxyInfo['IP'] = proxy.split(':')[0]
				proxyInfo['Port'] = proxy.split(':')[1]
				proxyInfo['Ping'] = getPing('http://www.adidas.com/')
				proxyInfo['ConnectTime'] = returnTime()
				info.append(proxyInfo)
			except:
				pass
	print(info)
	return render_template("index.html", gitCommits=gitCommits, proxyInfo=info)



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