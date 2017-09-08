import requests
import bs4
import random
import webbrowser
import csv
import threading
import RandomHeader
proxies = {
			'http': "",
			'https': "",
		}

ModelNumber = 'BB9043'
SizeList = [9, 13, 4, 10]
ThreadCount = 10

# Base URL =  http://www.adidas.com/us/BB9043.html?forceSelSize=BB9043_600
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def DoSomething():
	print('I just did something')

def URLGen(model, size):
	BaseSize = 580
	#Base Size is for Shoe Size 6.5
	ShoeSize = size - 6.5
	ShoeSize = ShoeSize * 20
	RawSize = ShoeSize + BaseSize
	ShoeSizeCode = int(RawSize)
	URL = 'http://www.adidas.com/us/' + str(model) + '.html?forceSelSize=' + str(model) + '_' + str(ShoeSizeCode)
	return URL
def CheckStock(url):
	RawHTML = requests.get(url, headers=RandomHeaders.LoadHeader(), proxies=proxies)
	Page = bs4.BeautifulSoup(RawHTML.text, "lxml")
	ListOfRawSizes = Page.select('.size-dropdown-block')
	Sizes = str(ListOfRawSizes[0].getText()).replace('\t', '')
	Sizes = Sizes.replace('\n\n', ' ')
	Sizes = Sizes.split()
	Sizes.remove('Select')
	Sizes.remove('size')
	return Sizes
def Main(model, size):
	url = URLGen(model, size)
	CheckStock(url, model)

def SneakerBot(model, size=None):
	while True:
		try:
			url = 'http://www.adidas.com/us/{}.html?'.format(model)
			Sizes = CheckStock(url)
			if size != None:
				#If you didn't input size
				if str(size) in Sizes:
					DoSomething()
			else:
				for a in Sizes:
					DoSomething()
		except:
			pass

threads = [threading.Thread(name='ThreadNumber{}'.format(n), target=SneakerBot, args(ModelNumber, size,)) for size in SizeList for n in range(ThreadCount)]
for t in threads: t.start()
