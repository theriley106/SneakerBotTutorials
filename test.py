import threading


def doIt():
	A = []
	
	def addToList(test):
		A.append(test)
	threads = [threading.Thread(target=addToList, args=("command",)) for i in range(20)]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	return A

testing = doIt()

print testing

