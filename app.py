import versionCheck
#^This fixes a really common problem I'm getting  messages about.  It checks for python 2.x
from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import requests
import sys
import bs4
import RandomHeaders
import re
import urllib
import threading
import time
import main
import csv
from time import gmtime, strftime

app = Flask(__name__)

PROXIES = [{}]




#bot = main.bot({})
#This initiates twice -- why??

def configure_proxy_settings(ip, port, username=None, password=None):
	"""
	Configuring proxies to pass to request
	:param ip: The IP address of the proxy you want to connect to ie 127.0.0.1
	:param port: The port number of the prxy server you are connecting to
	:param username: The username if requred authentication, need to be accompanied with a `password`.
	 Will default to None to None if not provided
	:param password: The password if required for authentication. Needs to be accompanied by a `username`
	 Will default to None if not provided
	:return: A dictionary of proxy settings
	"""
	proxies = None
	credentials = ''
	# If no IP address or port information is passed, in the proxy information will remain `None`
	# If no proxy information is set, the default settings for the machine will be used
	if ip is not None and port is not None:
		# Username and password not necessary
		if username is not None and password is not None:
			credentials = '{}:{}@'.format(username, password)

		proxies = {'http': 'http://{credentials}{ip}:{port}'.format(credentials=credentials, ip=ip, port=port),
				   'https': 'https://{credentials}{ip}:{port}'.format(credentials=credentials, ip=ip, port=port)
				   }

	return proxies


def getPing(url, ip, port, timeout=8):
	#If someone could make a better implementation of this that would be awesome
	proxies = None
	proxies = configure_proxy_settings(ip, port)
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			   'Accept-Language': 'en-US,en;q=0.9'
			   }
	start = time.time()
	nf = requests.get(url, proxies=proxies, headers=headers, timeout=timeout)
	page = nf.content
	nf.close()
	end = time.time()
	return format((end - start), '.5f')

def returnTime():
	#I know this doesn't adjust for local time - will fix this soon
	return strftime("%H:%M:%S", gmtime())

def massTestProxies(listOfProxies):
	RESPONSE = []
	def addToList(proxy):
		try:
			print("testing proxy: {}".format(proxy))
			proxyInfo = {}
			ip = proxy.partition(":")[0]
			port = proxy.partition(':')[2]
			url = 'http://www.adidas.com/'
			proxyInfo['IP'] = ip
			proxyInfo['Port'] = port
			proxyInfo['Ping'] = getPing('http://www.adidas.com/', ip=ip, port=port)
			proxyInfo['ConnectTime'] = returnTime()
			RESPONSE.append(proxyInfo)
		except:
			print("proxy: {} failed".format(proxy))


	threads = [threading.Thread(target=addToList, args=(proxy,)) for proxy in listOfProxies]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	return RESPONSE


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
		lastUpdate = page.select('relative-time')[0].getText()
		updateCount = int(re.findall('\d+', str(commitsCount[0].getText()))[0])
		return [lastUpdate, updateCount]
	except Exception as exp:
		print(exp)
		return "ERROR"

@app.route('/changeHeader', methods=['POST'])
def headerChange():
	#this is only printing the headers, but this will eventually change headers
	#print str(list(request.form.items())[0][1])
	bot.updateHeader(str(list(request.form.items())[0][1]))
	return redirect(url_for('index'))
	#perhaps it would be better to have default variables set for index, and this will edit default variables?
	# ie: index(headers=None, url=None, etc)

@app.route('/openDriver', methods=['POST'])
def driverAdd():
	bot.startAllDrivers()

@app.route('/', methods=['GET'])
def index():
	gitCommits = getCommits()
	lastUpdate = gitCommits[0]
	gitCommits = gitCommits[1]
	info = massTestProxies(PROXIES)
	
	print(info)
	return render_template("index.html", gitCommits=gitCommits, lastUpdate=lastUpdate, proxyInfo=info)



if __name__ == '__main__':
	try:
		bot = main.bot([{}])
	except:
		if raw_input("You need to install PhantomJS to use this program.  Continue without? [Y/N ").lower() == 'n':
			raise Exception("Install PhantomJS...")
	if len(sys.argv) > 1:
		if '.csv' in str(sys.argv[1]):
			PROXIES = returnProxies(sys.argv[1])
		if len(sys.argv) > 1 and '.csv' not in str(sys.argv[1]):
			for proxy in sys.argv[1:]:
				PROXIES.append(proxy)
		for proxy in PROXIES:
			bot.addProxy(proxy)
			print("Initiating Bot with Proxy: {}".format(proxy))
	else:
		print("It looks like you didn't input any Proxies.")
		if raw_input("It is HIGHLY recommended that you use proxies.  Continue without? [Y/N] ").lower() == 'n':
			raise Exception("Input Proxies...")
	app.run(host='127.0.0.1', port=8000, debug=True)