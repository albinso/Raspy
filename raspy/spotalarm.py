from datetime import datetime, time
from time import sleep
from subprocess import call
import sys

def act():
	"""
	Is called when the alarm goes off.
	Sends calls to mpc and ncmpcpp to
	control the mopidy server.
	"""
	call(["mpc", "volume", "0"])
	call(["ncmpcpp", "-h", "192.168.0.100", "prev"])
	call(["ncmpcpp", "play"])
	
	for i in range(100):
		call(["mpc", "volume", "+1"])
		sleep(1)

def wait_start(runTime, action):
	"""
	Calls action at time given by runTime.
	"""
	now = datetime.today().time()
	startTime = time(*(map(int, runTime.split(':'))))
	while startTime < now:
		# If startTime has already passed today we loop through this until midnight.
		sleep(60)
		now = datetime.today().time()

	while startTime > datetime.today().time():
		# While startTime is later today.
		sleep(60)
	return action()
	
if __name__ == '__main__':
	wait_start(sys.argv[1], act)
