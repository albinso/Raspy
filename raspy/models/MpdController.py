from subprocess import call, Popen, STDOUT
import os
import time

class MpdController:

	def __init__(self, default_volume=100):
		FNULL = open(os.devnull, 'w')
		self.process = Popen(["mopidy"], stdout=FNULL, stderr=STDOUT)
		code = 1
		while code != 0:
			code = self.set_volume(default_volume)
			time.sleep(1)
		call(['mpc', '-p', '6680', 'load', 'Cheese it (by heerkip)'])
		self.vol = default_volume

	def set_volume(self, vol):
		self.vol = vol
		return call(['mpc', '-p', '6680', 'volume', str(vol)])

	def get_volume(self):
		return self.vol

