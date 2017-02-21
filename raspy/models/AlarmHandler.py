from raspy.models.Alarm import Alarm

class AlarmHandler:
	def __init__(self):
		self.keygen = 0
		self.alarms = list()

	def create_alarm(self, time):
		alarm = Alarm(self.keygen, time)
		self.keygen += 1
		self.add_alarm(alarm)
		return alarm

	def add_alarm(self, alarm):
		self.alarms.append(alarm)

	def get_active_alarms(self):
		actives = list()
		for alarm in self.alarms:
			if alarm.is_active():
				actives.append(alarm)
		return actives

	def kill_by_key(self, key):
		n = 0
		for alarm in self.alarms:
			if alarm.matches(key):
				n += 1
				alarm.stop()
		return n

	def remove_inactive_alarms(self):
		for alarm in self.alarms:
			if not alarm.is_active():
				self.alarms.remove(alarm)