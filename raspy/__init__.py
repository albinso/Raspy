from flask import Flask
from models.AlarmHandler import AlarmHandler
from models.api_gen import AlarmApiGenerator

app = Flask(__name__, template_folder='templates', static_folder='static')
app.url_map.strict_slashes = False

alarm_handler = AlarmHandler()
api_gen = AlarmApiGenerator(alarm_handler)