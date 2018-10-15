from selenium import webdriver
import selenium.webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import sys

driver_info = sys.argv[1]

driver_info = json.load(open(driver_info))
print driver_info['cookies']
driver = webdriver.Firefox()
#replaces phantomjs instance with firefox browser
driver.get(driver_info['current_url'])
for cookie in driver_info['cookies']:
	driver.add_cookie(cookie)
driver.get(driver_info['current_url'])
