from subprocess import call, Popen
from datetime import datetime, time
import thread
from time import sleep

class Alarm:
	"""
	A single scheduled alarm. Controls the separate alarm process.
	Does not persist between sessions so if you restart the server all alarms are lost.
	"""
	def __init__(self, key, alarm_time, mpd_controller, light_controller):
		"""
		:key - A unique identifier for this alarm. Needs only be unique for the current session.
		:time - 24-hour time string on the format HH:MM
		"""
		self.alarm_time = alarm_time
		self.verify_time(alarm_time)
		self.key = key
		self.start()
		self.is_killed = False
		self.mpd_controller = mpd_controller
		self.light_controller = light_controller

	def verify_time(self, alarm_time):
		time(*(map(int, alarm_time.split(':'))))

	def get_process(self):
		return self.process

	def start(self):
		self.process = thread.start_new_thread(self.wait_start, ())

	def stop(self):
		"""
		Kills the process, effectively stopping the alarm from going off.
		Will not do anything once the alarm has been triggered.
		"""
		self.is_killed = True

	def is_active(self):
		return not self.is_killed

	def trigger(self):
		"""
		Is called when the alarm goes off.
		Sends calls to mpc and ncmpcpp to
		control the mopidy server.
		"""
		mpd_controller.set_volume(0)
		mpd_controller.prev()
		mpd_controller.play()
		light_controller.light_on()
		
		for i in range(50):
			mpd_controller.set_volume(2*i)
			sleep(1)

	def wait_start(self):
		"""
		Calls action at time given by runTime.
		"""
		now = datetime.today().time()
		startTime = time(*(map(int, self.alarm_time.split(':'))))
		while startTime < now:
			if self.is_killed:
				return
			# If startTime has already passed today we loop through this until midnight.
			sleep(1)
			now = datetime.today().time()

		while startTime > datetime.today().time():
			if self.is_killed:
				return
			# While startTime is later today.
			sleep(1)
		return self.trigger()

	def matches(self, key):
		return self.key == key

	def __eq__(self, other):
		return self.alarm_time == other.alarm_time and self.key == other.key

	def __ne__(self, other):
		return not self == other

	def __str__(self):
		return str(self.alarm_time)
