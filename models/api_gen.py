import json

class AlarmApiGenerator:
	def __init__(self, alarm_handler):
		self.alarm_handler = alarm_handler

	def get_alarms(self):
		data = {}
		for alarm in self.alarm_handler.get_active_alarms():
			data[str(alarm.key)] = str(alarm.time)
		js = json.dumps(data)
		return Response(js, status=200, mimetype='application/json')

	def remove_alarm_by_key(self, key):
		n = alarms.kill_by_key(key)
		data = {'key': str(key), 'n_killed': str(n)}
		js = json.dumps(data)
		resp = Response(js, status=200, mimetype='application/json')
		if n == 0:
			resp = Response(js, status=404, mimetype='application/json')
		return resp

	def create_alarm(self, time):
		alarm = self.alarm_handler.create_alarm(time)
		data = {'key': str(key)}
		js = json.dumps(data)
		resp = Response(js, status=200, mimetype='application/json')
		return resp

