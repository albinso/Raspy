import unittest
from raspy.models.AlarmHandler import AlarmHandler
from raspy.models.api_gen import AlarmApiGenerator
from raspy.models.MpdController import MpdController
import json
import ast
import pytest

class AlarmApiTest(unittest.TestCase):

	def setUp(self):
		self.alarm_handler = AlarmHandler()
		self.mpd_controller = MpdController()
		self.api = AlarmApiGenerator(self.alarm_handler, self.mpd_controller)

	def _make_alarm_from_time_and_get_alarms_response(self, time):
		self.api.create_alarm(time)
		return self.alarm_handler.alarms

	def _get_json_dict_from_response(self, resp):
		data = resp.get_data()
		data = ast.literal_eval(data)
		return data

	def test_create_alarm(self):
		time = "05:55"
		alarms = self._make_alarm_from_time_and_get_alarms_response(time)
		assert len(alarms) == 1
		assert alarms[0].alarm_time == time

	def test_create_alarm_with_invalid_time(self):
		time = "25:69"
		with pytest.raises(ValueError):
			self.api.create_alarm(time)

	def test_get_alarm(self):
		time1 = "02:00"
		time2 = "03:35"
		self.api.create_alarm(time1)
		self.api.create_alarm(time2)
		resp = self.api.get_alarms_response()
		data = self._get_json_dict_from_response(resp)
		assert resp.status_code == 200
		assert data['0'] == time1
		assert data['1'] == time2

	def test_remove_no_alarms(self):
		resp = self.api.remove_alarm_by_key(0)
		assert resp.status_code == 404

	def test_remove_alarm(self):
		self.api.create_alarm("05:55")
		resp = self.api.remove_alarm_by_key(0)
		assert resp.status_code == 200
		assert len(self.alarm_handler.alarms) == 0

	def tearDown(self):
		pass

if __name__ == '__main__':
	unittest.main()