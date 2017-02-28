import unittest
from raspy.models.MpdController import MpdController

class MpdControllerTest(unittest.TestCase):

	def setUp(self):
		ip = 'localhost'
		port = 6680
		self.controller = MpdController()

	def test_set_volume(self):
		vol = 50
		code = self.controller.set_volume(vol)
		actual_vol = self.controller.get_volume()
		self.assertEquals(code, 0)
		self.assertEquals(vol, actual_vol)

		
