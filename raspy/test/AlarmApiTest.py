import unittest
from raspy.models.AlarmHandler import AlarmHandler
from raspy.models.api_gen import AlarmApiGenerator
import json
import ast

class AlarmApiTest(unittest.TestCase):

	def setUp(self):
		self.alarm_handler = AlarmHandler()
		self.api = AlarmApiGenerator(self.alarm_handler)

	def _make_alarm_from_time_and_get_alarms_response(self, time):
		self.api.create_alarm(time)
		return self.alarm_handler.alarms

	def test_create_alarm(self):
		time = "05:55"
		alarms = self._make_alarm_from_time_and_get_alarms_response(time)
	
		self.assertEquals(len(alarms), 1)
		self.assertEquals(alarms[0].alarm_time, time)

	def test_create_alarm_with_invalid_time(self):
		time = "25:69"
		self.assertRaises(ValueError, self.api.create_alarm, time)

	def test_get_alarm(self):
		time1 = "02:00"
		time2 = "03:35"
		self.api.create_alarm(time1)
		self.api.create_alarm(time2)
		resp = self.api.get_alarms_response()
		data = resp.get_data()
		data = ast.literal_eval(data)
		self.assertEquals(resp.status_code, 200)
		self.assertEquals(data['0'], time1)
		self.assertEquals(data['1'], time2)

	def test_remove_no_alarms(self):
		resp = self.api.remove_alarm_by_key(0)
		self.assertEquals(resp.status_code, 204)

	def test_remove_alarm(self):
		self.api.create_alarm("05:55")
		resp = self.api.remove_alarm_by_key(0)
		self.assertEquals(resp.status_code, 200)
		self.assertEquals(len(self.alarm_handler.alarms), 0)

	def tearDown(self):
		pass

if __name__ == '__main__':
	unittest.main()