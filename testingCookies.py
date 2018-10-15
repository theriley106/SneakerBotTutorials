from selenium import webdriver
import selenium.webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
	"(KHTML, like Gecko) Chrome/15.0.87"
)

def save_driver(fileName, driver_info):
	with open(fileName, 'w') as fout:
		json.dump(driver_info, fout)

def convertHeadless(driver, url):
	#converts a phantomjs browser to a firefox webdriver window
	driver_info = {}
	driver_info['current_url'] = driver.current_url
	driver_info['cookies'] = driver.get_cookies()
	#saves cookies as dict
	save_driver("driver_info.json", driver_info)
	driver.quit()
	#closes the phantomjs window
	driver = webdriver.Firefox()
	#replaces phantomjs instance with firefox browser
	driver.get(url)
	for cookie in driver_info['cookies']:
		driver.add_cookie(cookie)
	driver.get(url)
	return driver

driver = webdriver.PhantomJS(desired_capabilities=dcap)
#driver = webdriver.Firefox()
driver.set_window_size(700,500)
driver.get('https://www.amazon.com/dp/047076905X')

driver.find_element_by_id("add-to-cart-button").click()

driver.get('https://www.amazon.com/gp/cart/view.html/ref=nav_cart')
new = convertHeadless(driver, 'https://www.amazon.com/gp/cart/view.html/ref=nav_cart')



