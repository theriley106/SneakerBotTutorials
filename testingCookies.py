from selenium import webdriver
import os
import requests
import bs4
import re
import selenium.webdriver
import RandomHeaders
import threading
import sys
import main
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
    "(KHTML, like Gecko) Chrome/15.0.87"
)
def convertHeadless(driver, url):
	#converts a phantomjs browser to a firefox webdriver window
	cookies = driver.get_cookies()
	#saves cookies as dict
	driver.quit()
	#closes the phantomjs window
	driver = webdriver.Firefox()
	#replaces phantomjs instance with firefox browser
	driver.get(url)
	for cookie in cookies:
		driver.add_cookie(cookie)
	driver.get(url)
	return driver

driver = webdriver.PhantomJS(desired_capabilities=dcap)
driver.set_window_size(1400,1000)
driver.get('https://www.amazon.com/dp/047076905X')

driver.find_element_by_id("add-to-cart-button").click()

driver.get('https://www.amazon.com/gp/cart/view.html/ref=nav_cart')
new = convertHeadless(driver, 'https://www.amazon.com/gp/cart/view.html/ref=nav_cart')