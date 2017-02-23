import unittest
from raspy.models.AlarmHandler import AlarmHandler
from raspy.models.Alarm import Alarm
import time

class AlarmHandlerTest(unittest.TestCase):

	def setUp(self):
		self.alarm_handler = AlarmHandler()

	def _make_n_alarms(self, n, time):
		for _ in range(n):
			self.alarm_handler.create_alarm(time)

	def test_create_first_alarm(self):
		time = "05:55"
		manual_alarm = Alarm(0, time)
		self.alarm_handler.create_alarm(time)
		factory_alarm = self.alarm_handler.alarms[0]
		self.assertEquals(factory_alarm, manual_alarm)

	def test_key_generation(self):
		time = "06:30"
		n_alarms = 15
		for _ in range(n_alarms):
			self.alarm_handler.create_alarm(time)
		alarms = self.alarm_handler.alarms

		self.assertEquals(len(alarms), n_alarms)
		for key in range(n_alarms):
			self.assertEquals(alarms[key].key, key)

	def test_kill_by_key(self):
		alarm_time = "13:00"
		n_alarms = 15
		delay = 1E-2 # Ensure process is shut down within this time
		self._make_n_alarms(n_alarms, alarm_time)
		alarms = self.alarm_handler.alarms
		key = 7
		n = self.alarm_handler.kill_by_key(key)
		self.assertEquals(n, 1)
		time.sleep(delay)
		self.assertFalse(alarms[key].is_active())

