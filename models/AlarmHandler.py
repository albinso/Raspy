from models.Alarm import Alarm

class AlarmHandler:
	def __init__(self):
		self.keygen = 0
		self.alarms = list()

	def create_alarm(self, time):
		print(self.__dict__)
		alarm = Alarm(self.keygen, time)
		self.keygen += 1
		self.add_alarm(alarm)

	def add_alarm(self, alarm):
		self.alarms.append(alarm)

	def get_active_alarms(self):
		actives = list()
		for alarm in self.alarms:
			proc = alarm.get_process()
			proc.poll()
			if proc.returncode == None:
				actives.append(alarm)
		return actives

	def remove_inactive_alarms(self):
		for alarm in self.alarms:
			proc = alarm.get_process()
			proc.poll()
			if proc.returncode != None:
				self.alarms.remove(alarm)