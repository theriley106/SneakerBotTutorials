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

app = Flask(__name__, static_url_path='/static')
# Sets the static folder
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# Flask settings
PROXIES = []
# Defines initial proxy list
sessionInfo = {}
# Info about this specific browser session
bot = main.bot([])
#bot is initated with a LIST of STRINGS for proxies... not dicts
TEST_URL = 'http://www.adidas.com/'
# For the proxy test

@app.after_request
# No caching at all for API endpoints.
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

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
	proxies = configure_proxy_settings(ip, port)
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			   'Accept-Language': 'en-US,en;q=0.9'
			   }
	start = time.time()
	# Start time
	nf = requests.get(url, proxies='{}:{}'.format(ip, port), headers=headers, timeout=timeout)
	# Makes Request
	page = nf.content
	# Makes sure it's succesful
	nf.close()
	# Closes out the request
	end = time.time()
	# Gets the total time
	return format((end - start), '.5f')
	# Returns the ping

def returnTime():
	# I know this doesn't adjust for local time - will fix this soon
	return strftime("%H:%M:%S", gmtime())

def massTestProxies(listOfProxies):
	# Tests all proxies in the list of proxies
	RESPONSE = []
	# This is a list of python dictionaries containing information about the proxies
	def addToList(proxy):
		try:
			print("testing proxy: {}".format(proxy))
			proxyInfo = {}
			ip = proxy.partition(":")[0]
			# Extracts address
			port = proxy.partition(':')[2]
			# Extracts port
			url = TEST_URL
			# Sets the URL to TEST_URL constant
			proxyInfo['IP'] = ip
			# IP Address
			proxyInfo['Port'] = port
			# Port Number
			proxyInfo['Ping'] = getPing('https://whatismyipaddress.com/', ip=ip, port=port)
			# Sets ping
			proxyInfo['ConnectTime'] = returnTime()
			# Time that the proxy was tested
			RESPONSE.append(proxyInfo)
			# Appends info
			print("done: {}".format(proxy))
			# Output saying the proxy was succesful
		except Exception as exp:
			# This means the proxy failed
			print exp
			# Prints the exception string
			print("proxy: {} failed".format(proxy))
		return
	threads = [threading.Thread(target=addToList, args=(proxy,)) for proxy in listOfProxies]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	return RESPONSE
	# Returns the list of proxy details

def returnProxies(csvpath):
	# Opens the proxy CSV
	with open(csvpath, 'rb') as f:
		reader = csv.reader(f)
		return list(reader)

def getCommits():
	for i in range(5):
		# Loops through five times or until it is successful
		try:
			url = 'https://github.com/theriley106/SneakerBotTutorials'
			res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
			# Pulls the page
			page = bs4.BeautifulSoup(res.text, 'lxml')
			# Parses the HTML
			updateCount = str(page).partition('<span class="num text-emphasized">')[2].partition("<")[0].strip()
			# This is the element that contains the commit count
			lastUpdate = page.select('relative-time')[0].getText()
			# This is the time of the last update
			if len(updateCount) > 2:
				# This means it was successful
				return [lastUpdate, updateCount]
		except Exception as exp:
			pass
	return "ERROR"

@app.route('/changeHeader', methods=['POST'])
def headerChange():
	#this is only printing the headers, but this will eventually change headers
	#print str(list(request.form.items())[0][1])
	bot.updateHeader(str(list(request.form.items())[0][1]))
	# Updates header to the one inputted into the site
	return redirect(url_for('useBot'))
	#perhaps it would be better to have default variables set for index, and this will edit default variables?
	# ie: index(headers=None, url=None, etc)

@app.route('/goToURL', methods=['POST'])
def goToURL():
	#this is only printing the headers, but this will eventually change headers
	#print str(list(request.form.items())[0][1])
	bot.sendAllToURL(url=str(list(request.form.items())[0][1]))
	# Send all of the browser windows to the URL inputted into the web app
	return redirect(url_for('useBot'))

@app.route('/openDriver', methods=['POST'])
def driverAdd():
	# Opens all drivers
	bot.startAllDrivers()

@app.route('/', methods=['GET'])
def index():
	# First parge
	gitCommits = getCommits()
	# Grabs the current amount of Git Commits
	sessionInfo['lastUpdate'] = gitCommits[0]
	# Last commit time
	sessionInfo['gitCommits'] = gitCommits[1]
	# Total number of commits
	sessionInfo['info'] = massTestProxies(PROXIES)
	# Contains info about the proxies being used
	print("Done mass test")
	bot.startAllDrivers()
	# Starts all drivers
	return redirect(url_for('useBot'))

@app.route('/botInfo', methods=['GET'])
def useBot():
	proxyLists = []
	# List of the proxies being used
	for proxy in bot.successProxies:
		# Goes through a list of all the working proxies
		proxyLists.append(proxy.partition(':')[0])
		# Only appends the ip
	return render_template("index.html", gitCommits=sessionInfo['gitCommits'], lastUpdate=sessionInfo['lastUpdate'], URL=bot.targetURL, proxyInfo=sessionInfo['info'], driverInfo=bot.driverInfo, proxyDiff=len(bot.failedProxies), allProxies=proxyLists)

@app.route('/test', methods=['GET'])
def testTemplate():
	# This is just a test page to make sure everything is working properly
	return render_template("index.html", gitCommits=100, lastUpdate='Dec 3', proxyInfo=[{"IP": '41', "Port": '41', "Ping": '132', "ConnectTime": '321'}], driverInfo=[{'proxy': 'proxy', 'driver': 'driver', 'url': 'url', 'useragent': 'self.headers'}], proxyDiff=4)


if __name__ == '__main__':
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
		if 'bypass' not in sys.argv:
			if raw_input("It is HIGHLY recommended that you use proxies.  Continue without? [Y/N] ").lower() == 'n':
				raise Exception("Input Proxies...")
	if 'admin' in str(sys.argv).lower():
		r = requests.post("http://138.197.123.15:8888/proxies/{}".format(open('../../SecretCode.txt').read().strip())).json()
		PROXIES = r["proxies"][-10:]
	try:
		bot = main.bot(PROXIES)
	except:
		if raw_input("You need to install PhantomJS to use this program.  Continue without? [Y/N ").lower() == 'n':
			raise Exception("Install PhantomJS...")
	app.run(host='0.0.0.0', port=8000)
