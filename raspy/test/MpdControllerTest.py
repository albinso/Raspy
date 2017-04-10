import unittest
from raspy.models.MpdController import MpdController
import pytest

class MpdControllerTest(unittest.TestCase):

	def setUp(self):
		ip = 'localhost'
		port = 6680
		self.controller = MpdController()

	def test_set_volume(self):
		vol = 50
		code = self.controller.set_volume(vol)
		actual_vol = self.controller.get_volume()
		assert code == 0
		assert vol == actual_vol

	def test_get_playlists(self):
		playlists = self.controller.get_playlists()
		print('Playlists ', playlists)
		assert len(playlists) > 0
		assert 'Magic Tavern' in playlists


		
