import json
from flask import Response

class AlarmApiGenerator:
	def __init__(self, alarm_handler):
		self.alarm_handler = alarm_handler

	def get_alarms_response(self):
		data = {}
		for alarm in self.alarm_handler.get_active_alarms():
			data[str(alarm.key)] = str(alarm.alarm_time)
		js = json.dumps(data)
		return Response(js, status=200, mimetype='application/json')

	def remove_alarm_by_key(self, key):
		found = self.alarm_handler.kill_by_key(key)
		self.alarm_handler.remove_inactive_alarms()
		data = {'key': str(key), 'found': str(found)}
		code = 200
		if not found:
			code = 404
		return self.dict_to_json_response(data, status=code)

	def create_alarm(self, time):
		alarm = self.alarm_handler.create_alarm(time)
		data = {'key': str(alarm.key)}
		return self.dict_to_json_response(data, status=200)

	def dict_to_json_response(self, data, status):
		js = json.dumps(data)
		return Response(js, status=status, mimetype='application/json')

