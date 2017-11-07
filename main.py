from selenium import webdriver
import os
import requests
import bs4
import re
import selenium.webdriver
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.32 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.32"}
class attempt(object):
	def __init__(self, proxy):
		print('Initiated')
		self.proxy = proxy

def MakeTrade(ticker, quantity, username, password):
	proxies = {}
	s = requests.Session()
	data = {'form_id':'account_api_form', 'email': username,
	'password': password, 'op': 'Sign In'}
	url = 'http://www.investopedia.com/accounts/login.aspx'
	r = s.post(url, data=data, headers=headers, proxies=proxies)
	r = s.get('http://www.investopedia.com/simulator/portfolio/', data=data, headers=headers, proxies=proxies)
	soup = bs4.BeautifulSoup(r.text, 'lxml')
	AccountValue = soup.select('p')[0].getText()
	print AccountValue
	r = s.post('http://www.investopedia.com/simulator/ajax/quotebox.aspx', headers=headers, data={'symbol': "AAPL"})
	r = s.get('http://www.investopedia.com/simulator/trade/tradestock.aspx', headers=headers)
	page = bs4.BeautifulSoup(r.text, 'lxml')
	for e in page.find_all("input", type="hidden"):
		if "formToken" in str(e):
			Form_ID = str(e).partition('type="hidden" value="')[2].partition('"/>')[0]
	data = {'formToken': str(Form_ID), 'symbolTextbox':ticker,
	'symbolTextbox_mi_1_value':'AAPL',
	'selectedValue':ticker,
	'transactionTypeDropDown':'1',
	'quantityTextbox':quantity,
	'isShowMax':'0',
	'Price':'Market',
	'limitPriceTextBox':'',
	'stopPriceTextBox':'',
	'tStopPRCTextBox':'',
	'tStopVALTextBox':'',
	'durationTypeDropDown':'2',
	'sendConfirmationEmailCheckBox':'on'}
	r = s.post('http://www.investopedia.com/simulator/trade/tradestock.aspx', headers=headers, data=data)
	return s.cookies

def openWindow(url, c):
	driver = webdriver.FirefoxProfile()
	driver.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.32 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.32")
	driver = webdriver.Firefox(driver)
	driver.get('http://www.investopedia.com/simulator/trade/tradestock.aspx')
	driver.add_cookie(driver.add_cookie({'name': c.name, 'value': c.value, 'path': c.path, 'expiry': c.expires}))
	driver.get('http://www.investopedia.com/simulator/trade/tradestock.aspx')
