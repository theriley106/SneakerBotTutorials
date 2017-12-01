import sys
import time

if (sys.version_info > (3, 0)):
	print("You're trying to run this on Python 3.x - This is a Python 2.7 Program\n")
	time.sleep(1)
	sys.exit()