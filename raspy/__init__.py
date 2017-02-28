from flask import Flask
from raspy.models.AlarmHandler import AlarmHandler
from raspy.models.api_gen import AlarmApiGenerator
from raspy.models.MpdController import MpdController

app = Flask(__name__, template_folder='templates', static_folder='static')
app.url_map.strict_slashes = False

alarm_handler = AlarmHandler()
mpd_controller = MpdController()
api_gen = AlarmApiGenerator(alarm_handler, mpd_controller)

