
def get_configs():
	with open('config.txt', 'r') as f:
		content = f.readlines()

	confs = dict()
	for line in content:
		vals = line.split('=')
		key = vals[0]
		val = vals[1]
		confs[key] = val
	return confs

		