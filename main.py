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
	BaseSize = 580
	#Base Size is for Shoe Size 6.5
	ShoeSize = size - 6.5
	ShoeSize = ShoeSize * 20
	RawSize = ShoeSize + BaseSize
	ShoeSizeCode = int(RawSize)
	URL = 'http://www.adidas.com/us/' + str(model) + '.html?forceSelSize=' + str(model) + '_' + str(ShoeSizeCode)
	return URL

def createHeadlessBrowser(proxy=None, XResolution=1024, YResolution=768):
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = (
	    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36')
	if proxy != None:
		service_args = ['--proxy={}'.format(proxy),'--proxy-type=https','--ignore-ssl-errors=true',]
		driver = webdriver.PhantomJS(service_args=service_args, desired_capabilities=dcap)
	else:
		driver = webdriver.PhantomJS(desired_capabilities=dcap)
	driver.set_window_size(XResolution,YResolution)
	driver.set_page_load_timeout(20)
	return driver




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
		self.driverList = []
		self.driverInfo = []

	def updateHeader(self, userAgent):
		#placeholder function for proxy change
		self.headers = {'User-Agent': userAgent}
		print self.headers

	def addProxy(self, proxy):
		self.proxyList.append(proxy)
		print("Successfully added {}".format(proxy))

	def startDriver(self, proxy=None, url='https://www.reddit.com/r/cscareerquestions/'):
		if proxy != None:
			print proxy
			driver = createHeadlessBrowser(proxy=proxy)
		else:
			driver = createHeadlessBrowser()
		try:
			driver.get(url)
		except:
			driver.close()
		self.driverList.append(driver)
		self.driverInfo.append({'proxy': proxy, 'driver': driver, 'url': url, 'useragent': self.headers})
		
		#this is just a placeholder url
		if self.saveSS == True:
			driver.save_screenshot('static/{}.png'.format(proxy.partition(':')[0]))
		print("started {} driver".format(proxy))


	def startAllDrivers(self):
		threads = [threading.Thread(target=self.startDriver, args=(proxy,)) for proxy in self.proxyList]
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join()

	def returnDriverInfo(self):
		return self.driverInfo

		




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
