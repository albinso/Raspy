from subprocess import call, Popen

class Alarm:
	"""
	A single scheduled alarm. Controls the separate alarm process.
	Does not persist between sessions so if you restart the server all alarms are lost.
	"""
	def __init__(self, key, time):
		"""
		:key - A unique identifier for this alarm. Needs only be unique for the current session.
		:time - 24-hour time string on the format HH:MM
		"""
		self.time = time
		self.key = key
		self.process = Popen(["python", "spotalarm.py", time])

	def get_process(self):
		return self.process

	def stop(self):
		"""
		Kills the process, effectively stopping the alarm from going off.
		Will not do anything once the alarm has been triggered.
		"""
		self.process.kill()

	def is_active(self):
		proc = self.get_process()
		proc.poll()
		return proc.returncode == None

	def matches(self, key):
		return self.key == key

	def __str__(self):
		return str(self.time)
