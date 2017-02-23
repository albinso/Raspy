from subprocess import call, Popen
from datetime import time

class Alarm:
	"""
	A single scheduled alarm. Controls the separate alarm process.
	Does not persist between sessions so if you restart the server all alarms are lost.
	"""
	def __init__(self, key, alarm_time):
		"""
		:key - A unique identifier for this alarm. Needs only be unique for the current session.
		:time - 24-hour time string on the format HH:MM
		"""
		self.alarm_time = alarm_time
		self.verify_time(alarm_time)
		self.key = key
		self.process = Popen(["python", "raspy/spotalarm.py", self.alarm_time])
		self.is_killed = False

	def verify_time(self, alarm_time):
		time(*(map(int, alarm_time.split(':'))))

	def get_process(self):
		return self.process

	def stop(self):
		"""
		Kills the process, effectively stopping the alarm from going off.
		Will not do anything once the alarm has been triggered.
		"""
		if self.is_active():
			self.process.kill()
			self.is_killed = True

	def is_active(self):
		proc = self.get_process()
		proc.poll()
		return proc.returncode == None and not self.is_killed

	def matches(self, key):
		return self.key == key

	def __eq__(self, other):
		return self.alarm_time == other.alarm_time and self.key == other.key

	def __ne__(self, other):
		return not self == other

	def __str__(self):
		return str(self.time)
