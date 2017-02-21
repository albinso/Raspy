import unittest
from raspy import app

class AlarmApiTest(unittest.TestCase):

	def setUp(self):
		app.config['Testing'] = True
		self.app = app.test_client()

	def test_app(self):
		self.assertFalse(True)

	def tearDown(self):
		pass

if __name__ == '__main__':
	unittest.main()