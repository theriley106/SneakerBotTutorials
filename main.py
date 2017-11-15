from selenium import webdriver
import os
import requests
import bs4
import re
import selenium.webdriver
import RandomHeaders
import threading
import sys
URL = sys.argv[2]
PROXIES = sys.argv[2:]


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
	def __init__(self, proxy, saveimages=True):
		print('Initiated')
		self.proxy = proxy
		self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		self.driver = webdriver.PhantomJS(service_args=['--proxy={}'.format(proxy), '--proxy-type=http'])
		self.driver.get('https://www.reddit.com/r/cscareerquestions/')



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
	SPLASHTITLE = grabCurrentTitle(URL)
	threads = [threading.Thread(target=grabSS, args=(proxy,)) for proxy in PROXIES]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
