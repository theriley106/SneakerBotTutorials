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
SPLASHTITLE = grabCurrentTitle(URL)
class bot(object):
	def __init__(self, proxy):
		print('Initiated')
		self.proxy = proxy
		self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		self.driver = webdriver.PhantomJS(service_args=['--proxy={}'.format(proxy), '--proxy-type=http'])
		self.driver.get('https://www.reddit.com/r/cscareerquestions/')

def grabCurrentTitle(url):
	#this grabs the title of the splash page
	driver = webdriver.PhantomJS()
	driver.get(url)
	title = driver.title
	driver.close()
	driver.quit()
	return title

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
			driver = webdriver.Firefox()
			for cookie in cookies_list:
				driver.add_cookie(cookie)
				#converts phantomjs cookies into firefox webdriver to check out
			driver.get(URL)


		except Exception as exp:
			print exp
if __name__ == "__main__":
	threads = [threading.Thread(target=grabSS, args=(proxy,)) for proxy in PROXIES]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
