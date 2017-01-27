# Base URL =  http://www.adidas.com/us/BB9043.html?forceSelSize=BB9043_600
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def URLGen(model, size):
	BaseSize = 580
	#Base Size is for Shoe Size 6.5
	ShoeSize = size - 6.5
	ShoeSize = ShoeSize * 20
	RawSize = ShoeSize + BaseSize
	ShoeSizeCode = int(RawSize)
	URL = 'http://www.adidas.com/us/' + str(model) + '.html?forceSelSize=' + str(model) + '_' + str(ShoeSizeCode)
	return URL

Model = raw_input('Model #: ')
Size = input('Size: ')

URL = URLGen(Model, Size)

print(URL)