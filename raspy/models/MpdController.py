from subprocess import call, Popen, STDOUT
import os

class MpdController:

	def __init__(self):
		FNULL = open(os.devnull, 'w')
		self.process = Popen(["mopidy"], stdout=FNULL, stderr=STDOUT)
		self.vol = 100

	def set_volume(self, vol):
		self.vol = vol
		return call(['mpc', '-p', '6680', 'volume', str(vol)])

	def get_volume(self):
		return self.vol

