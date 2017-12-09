from selenium import webdriver
import os
import requests
import bs4
import re
import selenium.webdriver
import RandomHeaders
import threading
import sys

def URLGen(model, size):
	BaseSize = 580
	#Base Size is for Shoe Size 6.5
	ShoeSize = size - 6.5
	ShoeSize = ShoeSize * 20
	RawSize = ShoeSize + BaseSize
	ShoeSizeCode = int(RawSize)
	URL = 'http://www.adidas.com/us/' + str(model) + '.html?forceSelSize=' + str(model) + '_' + str(ShoeSizeCode)
	return URL

def grabCurrentTitle(url):
	#this grabs the title of the splash page
	driver = webdriver.PhantomJS()
	driver.get(url)
	title = driver.title
	driver.close()
	driver.quit()
	return title

def verifyProxy(proxy, timeout=10):
	#this is to verify that a proxy is working
	try:
		requests.get('https://www.google.com/', timeout=timeout)
	except:
		return False

class bot(object):
	#placeholder bot class - will eventually merge a ton of stuff into this
	def __init__(self, proxy, saveimages=True):
		print('Initiated bot')
		self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		self.proxyList = proxy
		self.saveSS = saveimages

	def updateHeader(self, userAgent):
		#placeholder function for proxy change
		self.headers = {'User-Agent': userAgent}
		print self.headers

	def addProxy(self, proxy):
		self.proxyList.append(proxy)
		print("Successfully added {}".format(proxy))

	def startDriver(self, proxy=None):
		if proxy != None:
			driver = webdriver.PhantomJS(service_args=['--proxy={}'.format(proxy), '--proxy-type=http'])
		else:
			driver = webdriver.PhantomJS()
		#thsi isn't actually using the header -- fix this soon
		driver.get('https://www.reddit.com/r/cscareerquestions/')
		#this is just a placeholder url
		if self.saveSS == True:
			driver.save_screenshot('{}.png'.format(proxy.replace(':', '')))


	def startAllDrivers(self):
		for proxy in self.proxyList:
			self.startDriver(proxy)
			print("started driver")
		




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
