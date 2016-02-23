import json

def log(request):
	print("logging")
	print(request.environ['REMOTE_ADDR'])