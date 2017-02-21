from flask import Flask
from raspy.models.AlarmHandler import AlarmHandler
from raspy.models.api_gen import AlarmApiGenerator

app = Flask(__name__, template_folder='templates', static_folder='static')
app.url_map.strict_slashes = False

alarm_handler = AlarmHandler()
api_gen = AlarmApiGenerator(alarm_handler)
