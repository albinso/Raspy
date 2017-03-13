from subprocess import call

class LightController:

	def light_on(self):
		code = '1010111011101010101010101'
		return call(['python', 'raspy/RFTransmitter.py', code])

	def light_off(self):
		code = '1010111011101010101010111'
		return call(['python', 'raspy/RFTransmitter.py', code])
