from selenium import webdriver
import os
import requests
import bs4
import re
import selenium.webdriver
import threading
class bot(object):
	def __init__(self, proxy):
		print('Initiated')
		self.proxy = proxy
		self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		self.driver = webdriver.PhantomJS(service_args=['--proxy={}'.format(proxy), '--proxy-type=http'])
		self.driver.get('https://www.reddit.com/r/cscareerquestions/')

def grabScreenSize(proxy):
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		driver = webdriver.PhantomJS(service_args=['--proxy={}'.format(proxy), '--proxy-type=https'])
		#driver = webdriver.PhantomJS()
		driver.get('https://www.privateinternetaccess.com/pages/whats-my-ip/')
		driver.save_screenshot('{}.png'.format(proxy.replace(':', '').replace('.', '')))
		driver.close()
		driver.quit()
	except Exception as exp:
		print exp
if __name__ == "__main__":
	r = requests.post("http://138.197.123.15:8888/proxies/{}".format(open('../../SecretCode.txt').read().strip())).json()
	proxies = r["proxies"][:10]
	threads = [threading.Thread(target=grabScreenSize, args=(proxy,)) for proxy in proxies]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
