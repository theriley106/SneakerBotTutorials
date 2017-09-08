from selenium import webdriver
import os
import requests
import re

class attempt(object):
	def __init__(self, proxy):
		print('Initiated')
		self.proxy = proxy