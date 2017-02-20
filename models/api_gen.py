class ApiGenerator:
	def __init__(self):
		pass

	def get_alarms(self, alarm_handler):
		data = {}
		for alarm in alarm_handler.get_active_alarms():
			data[str(alarm.key)] = str(alarm.time)
		return json.dumps(data)