import unittest
from raspy.models.AlarmHandler import AlarmHandler
from raspy.models.Alarm import Alarm
import time
import pytest

class AlarmHandlerTest(unittest.TestCase):

	def setUp(self):
		self.alarm_handler = AlarmHandler()
		self.standard_alarm_number = 5
		self.success_test_key = 3
		self.alarms = self.alarm_handler.alarms

	def _make_n_alarms(self, n, time):
		for _ in range(n):
			self.alarm_handler.create_alarm(time)

	def test_create_first_alarm(self):
		time = "05:55"
		manual_alarm = Alarm(0, time)
		self.alarm_handler.create_alarm(time)
		factory_alarm = self.alarm_handler.alarms[0]
		assert factory_alarm == manual_alarm

	def heavy_test_create_many_alarms(self):
		time = "06:00"
		n_alarms = self.standard_alarm_number*100
		self._make_n_alarms(n_alarms, time)
		assert len(self.alarms) == n_alarms

	def test_key_generation(self):
		time = "23:32"
		n_alarms = self.standard_alarm_number
		for _ in range(n_alarms):
			self.alarm_handler.create_alarm(time)

		assert len(self.alarms) == n_alarms
		for key in range(n_alarms):
			assert self.alarms[key].key == key

	def test_kill_by_key(self):
		alarm_time = "13:00"
		n_alarms = self.standard_alarm_number
		self._make_n_alarms(n_alarms, alarm_time)
		key = self.success_test_key
		n = self.alarm_handler.kill_by_key(key)
		assert n == 1
		assert not self.alarms[key].is_active()

	def test_kill_by_key_no_alarms(self):
		alarms = self.alarm_handler.alarms
		key = 0
		n = self.alarm_handler.kill_by_key(key)
		assert n == 0
		assert len(self.alarms) == 0

	def test_kill_by_key_invalid_key(self):
		alarm_time = "13:00"
		n_alarms = self.standard_alarm_number
		self._make_n_alarms(n_alarms, alarm_time)
		key = self.standard_alarm_number + 2
		n = self.alarm_handler.kill_by_key(key)
		assert n == 0
		assert len(self.alarms) == n_alarms

	def test_remove_inactive_alarms_len_single_case(self):
		alarm_time = "15:00"
		self.alarm_handler.create_alarm(alarm_time)
		key = 0
		self.alarm_handler.kill_by_key(0)
		self.alarm_handler.remove_inactive_alarms()
		assert 0 == len(self.alarms)

	def test_remove_inactive_alarms_len(self):
		alarm_time = "15:00"
		n_alarms = self.standard_alarm_number
		self._make_n_alarms(n_alarms, alarm_time)
		key = self.success_test_key
		self.alarm_handler.kill_by_key(key)
		self.alarm_handler.remove_inactive_alarms()
		assert n_alarms-1 == len(self.alarms)

