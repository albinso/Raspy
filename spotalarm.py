from datetime import datetime, time
from time import sleep
from subprocess import call
import sys

def act():
    call(["mpc", "volume", "100"])
    call(["ncmpcpp", "-h", "192.168.0.100", "prev"])
    call(["ncmpcpp", "play"])

def wait_start(runTime, action):
    now = datetime.today().time()
    startTime = time(*(map(int, runTime.split(':'))))
    while startTime < now:
    	sleep(60)
    	now = datetime.today().time()

    while startTime > datetime.today().time(): # you can add here any additional variable to break loop if necessary
        sleep(60) # you can change 1 sec interval to any other
    return act()

wait_start(sys.argv[1], act)
