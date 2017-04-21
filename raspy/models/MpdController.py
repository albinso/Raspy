from subprocess import call, Popen, STDOUT, check_output
import os
import time
import random

class MpdController:

	def __init__(self, default_volume=100):
		self.vol = default_volume
		self.process = self.init_mopidy()
		self.wait_for_mopidy_startup()
		self.playing = False
		playlist = random.choice(self.get_playlists())
		self.load_playlist(playlist)
		

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

	def raise_volume(self, change):
		self.vol = Math.min(self.vol + change, 100)
		return call(self.make_mpc_command(['volume', '+'+str(change)]))

	def lower_volume(self, change):
		self.vol = Math.max(self.vol - change, 0)
		return call(self.make_mpc_command(['volume', '-'+str(change)]))

	def get_volume(self):
		return self.vol

	def load_playlist(self, name):
		command = self.make_mpc_command(['load', name])
		return call(command)

	def play(self):
		if self.playing:
			print('Already playing so doing nothing')
			return 0
		self.playing = True
		command = self.make_mpc_command(['play'])
		return call(command)

	def pause(self):
		self.playing = False
		command = self.make_mpc_command(['pause'])
		return call(command)

	def next(self):
		command = self.make_mpc_command(['next'])
		return call(command)

	def prev(self):
		command = self.make_mpc_command(['prev'])
		return call(command)

	def get_playlists(self):
		command = self.make_mpc_command(['lsplaylists'])
		output = check_output(command)
		return output.split('\n')

	def make_mpc_command(self, *args):
		return ['mpc', '-p', '6680'] + args[0]

