import random
import csv


UserAgentCSV = open('UserAgent.csv', 'r')
UserAgentList = csv.reader(UserAgentCSV)
UserAgentList = [row for row in UserAgentList]
UserAgentList = [l[0] for l in UserAgentList]
random.shuffle(UserAgentList)

def LoadHeader():
	return {'User-Agent': random.choice(UserAgentList)}
