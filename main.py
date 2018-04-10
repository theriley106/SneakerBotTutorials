from selenium import webdriver
import os
import requests
import bs4
import re
import selenium.webdriver
import RandomHeaders
import threading
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
SS_FORMAT = "static/{0}.png"
VERBOSE_MODE = False

def convertHeadless(driver, url):
	#converts a phantomjs browser to a firefox webdriver window
	cookies = driver.get_cookies()
	#saves cookies as dict
	driver.quit()
	#closes the phantomjs window
	driver = webdriver.Firefox()
	#replaces phantomjs instance with firefox browser
	driver.get(url)
	# has to go to the url before adding cookies
	# If you were doing this with shoes - it should show an empty cart
	for cookie in cookies:
		#adds cookies to the driver
		driver.add_cookie(cookie)
	driver.get(url)
	# this will reload the url with the cookies you imported
	return driver

def URLGen(model, size):
	# Generates URLs for releases on Adidas.com
	BaseSize = 580
	#Base Size is for Shoe Size 6.5
	ShoeSize = size - 6.5
	ShoeSize = ShoeSize * 20
	RawSize = ShoeSize + BaseSize
	ShoeSizeCode = int(RawSize)
	URL = 'http://www.adidas.com/us/' + str(model) + '.html?forceSelSize=' + str(model) + '_' + str(ShoeSizeCode)
	return URL

def createHeadlessBrowser(proxy=None, XResolution=1024, YResolution=768, timeout=20):
	#proxy = None
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = (
	    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36')
	# Fake browser headers
	if proxy != None:
		# This means the user set a proxy
		service_args = ['--proxy={}'.format(proxy),'--proxy-type=https','--ignore-ssl-errors=true', '--ssl-protocol=any', '--web-security=false',]
		driver = webdriver.PhantomJS(service_args=service_args, desired_capabilities=dcap)
	else:
		# No proxy was set by the user
		driver = webdriver.PhantomJS(desired_capabilities=dcap)
	driver.set_window_size(XResolution,YResolution)
	# Sets the screen resolution
	# Ideally this will be dynamic based on the number of browsers open
	driver.set_page_load_timeout(timeout)
	# Sets the timeout for the selenium window
	return driver
	# Returns driver instance

def grabCurrentTitle(url):
	#this grabs the title of the splash page
	driver = webdriver.PhantomJS()
	# Creates new webdriver instance
	driver.get(url)
	# Navigates to the user
	title = driver.title
	# Gets the title.  eg: Adidas | Page Not Found
	driver.close()
	# Closes out the webdriver
	driver.quit()
	# Closes out the webdriver
	return title
	# Returns the title as a string

def verifyProxy(proxy, timeout=10):
	# This function is to verify that a proxy is working
	try:
		requests.get('https://www.google.com/', proxy=proxy, timeout=timeout)
		# Grabs google.com
		return True
		# True means the proxy is working
	except:
		# This means the .get function failed
		return False

class bot(object):
	#placeholder bot class - will eventually merge a ton of stuff into this
	def __init__(self, proxy, saveimages=True, url='https://www.google.com/'):
		self.headers = HEADERS
		# Defines the headers that the proxy will use
		self.proxyList = proxy
		# This contains all the proxies used by the bot
		if VERBOSE_MODE == True:
			print(self.proxyList)
			# Prints out all of the proxies in proxy list
		self.saveSS = saveimages
		# This tells the program to save all screenshots or not
		self.driverList = []
		# Contains a list of selenium instances
		self.driverInfo = []
		''' Contains a list of python dicts:
		{'proxy': proxy, 'driver': driver, 'url': self.targetURL, 'useragent': self.headers}
		'''
		self.failedProxies = []
		# This is an ongoing list of invalid proxies
		self.successProxies = []
		# This is an ongoing list of valid proxies
		self.targetURL = url
		#why are there so many... this is a bad way of doing this


	def updateHeader(self, userAgent):
		#placeholder function for proxy change
		self.headers = {'User-Agent': userAgent}
		if VERBOSE_MODE == True:
			print self.headers
			# Prints out the headers used by this driver

	def addProxy(self, proxy):
		self.proxyList.append(proxy)
		# Appends the proxy to the main list of proxies
		if VERBOSE_MODE == True:
			print("Successfully added {}".format(proxy))
			# Prints out the proxy ip

	def startDriver(self, proxy=None):
		if proxy != None:
			# This means the user defined the proxy on init
			driver = createHeadlessBrowser(proxy=proxy)
			# Starts a phantomJS instance with that proxy
		else:
			# The user did not define a proxy
			driver = createHeadlessBrowser()
			# Creates a phantomJS instance without a proxy
		try:
			# Tries to navigate to the URL
			driver.get(self.targetURL)
		except:
			# This means the navigation failed, and the proxy is likely not working
			driver.close()
			# Closes out the driver
			self.failedProxies.append(proxy)
			# Appends the proxy to the failed proxy list
			return
			# Returns none
		self.driverList.append({'driver': driver, 'proxy': proxy})
		# Appends the open webdriver instance to driverList
		self.driverInfo.append({'proxy': proxy, 'driver': driver, 'url': self.targetURL, 'useragent': self.headers})
		# Appens the open webdriver instance to the driverInfo list
		self.successProxies.append(proxy)
		# This adds the proxy to the list of working proxies
		if self.saveSS == True:
			# The program takes a screenshot
			driver.save_screenshot(SS_FORMAT.format(proxy.partition(':')[0]))
			# Saves the screenshot locally
		if VERBOSE_MODE == True:
			print("started {} driver".format(proxy))
			# Prints out the proxy ip for the webdriver instance

	def goToURL(self, driver):
		proxy = driver['proxy']
		# This is the proxy that is used that selenium driver instance
		driver = driver['driver']
		# This is the selenium webdriver instance
		driver.get(self.targetURL)
		# Goes to the url defined at init
		if VERBOSE_MODE == True:
			print driver.title
			# Prints the title of the page
		if self.saveSS == True:
			driver.save_screenshot(SS_FORMAT.format(proxy.partition(':')[0]))
			# Saves the screenshot
			print("saved screenshot on {} at {}.png".format(driver, proxy.partition(':')[0]))
			# This will print regardless of the VERBOSE_MODE constant


	def sendAllToURL(self, url):
		# Sends all of the open instances to a specified URL
		threads = [threading.Thread(target=self.goToURL, args=(driver, url)) for driver in self.driverList]
		# Creates a list of threads
		for thread in threads:
			# Starts all of them
			thread.start()
		for thread in threads:
			# Joins them together so they exit at the same time
			thread.join()


	def startAllDrivers(self):
		# Starts up all of the webdriver instances
		threads = [threading.Thread(target=self.startDriver, args=(proxy,)) for proxy in self.proxyList]
		# Creates a list of threads
		for thread in threads:
			# Starts all of them
			thread.start()
		for thread in threads:
			# Joins them together so they exit at the same time
			thread.join()






def grabSS(proxy):
	while True:
		try:
			headers = RandomHeaders.LoadHeader()
			driver = webdriver.PhantomJS(service_args=['--proxy={}'.format(proxy), '--proxy-type=https'])
			#driver = webdriver.PhantomJS()
			driver.get(URL)
			while driver.title == SPLASHTITLE:
				driver.save_screenshot('{}.png'.format(proxy.replace(':', '').replace('.', '')))
				#this just visualized the phantomjs driver - you can replace this with pass if you're trying to reduce mem
			cookies_list = driver.get_cookies()
			driver.close()
			driver.quit()
			driver = webdriver.Firefox(service_args=['--proxy={}'.format(proxy), '--proxy-type=https'])
			# you can only set cookies for the driver's current domain so visit the page first then set cookies
			driver.get(URL)
			# precautionary - delete all cookies first
			driver.delete_all_cookies()
			for cookie in cookies_list:
				# precautionary - prevent possible Exception - can only add cookie for current domain
				if "adidas" in cookie['domain']:
					driver.add_cookie(cookie)
			# once cookies are changed browser must be refreshed
			driver.refresh()
			#converts phantomjs cookies into firefox webdriver to check out

		except Exception as exp:
			print exp
if __name__ == "__main__":

	URL = sys.argv[2]
	if '-r' in str(sys.argv).lower():
		PROXIES = []
		with open(str(sys.argv[sys.argv.index('-R')+1])) as f:
			PROXIES = f.readlines()
	else:
		PROXIES = sys.argv[2:]
	SPLASHTITLE = grabCurrentTitle(URL)
	threads = [threading.Thread(target=grabSS, args=(proxy,)) for proxy in PROXIES]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
