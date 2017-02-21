import unittest
from raspy import app, api_gen, alarm_handler
from raspy.models.AlarmHandler import AlarmHandler
from raspy.models.api_gen import AlarmApiGenerator

class AlarmApiTest(unittest.TestCase):

	def setUp(self):
		self.alarm_handler = AlarmHandler()
		self.api = AlarmApiGenerator(self.alarm_handler)

	def _make_alarm_from_time_and_get_alarms(self, time):
		self.api.create_alarm(time)
		return self.alarm_handler.alarms

	def test_create_alarm(self):
		time = "05:55"
		alarms = self._make_alarm_from_time_and_get_alarms(time)
	
		self.assertEquals(len(alarms), 1)
		self.assertEquals(alarms[0].alarm_time, time)

	def test_create_alarm_with_invalid_time(self):
		time = "25:69"
		self.assertRaises(ValueError, self.api.create_alarm, time)

	def tearDown(self):
		pass

if __name__ == '__main__':
	unittest.main()