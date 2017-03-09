from subprocess import call, Popen, STDOUT
import os
import time

class MpdController:

	def __init__(self, default_volume=100):
		self.vol = default_volume
		self.process = self.init_mopidy()
		self.wait_for_mopidy_startup()
		self.load_playlist('Cheese it (by heerkip)')
		

	def init_mopidy(self):
		FNULL = open(os.devnull, 'w')
		return Popen(["mopidy"], stdout=FNULL, stderr=STDOUT)

	def wait_for_mopidy_startup(self):
		code = 1
		while code != 0:
			code = self.set_volume(self.vol)
			time.sleep(1)

	def set_volume(self, vol):
		self.vol = vol
		return call(self.make_mpc_command(['volume', str(vol)]))

	def get_volume(self):
		return self.vol

	def load_playlist(self, name):
		command = self.make_mpc_command(['load', name])
		return call(command)

	def play(self):
		command = self.make_mpc_command(['play'])
		return call(command)

	def pause(self):
		command = self.make_mpc_command(['pause'])
		return call(command)

	def next(self):
		command = self.make_mpc_command(['next'])
		return call(command)

	def make_mpc_command(self, *args):
		return ['mpc', '-p', '6680'] + args[0]

