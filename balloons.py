from run import RadarProcessRunner
from show_data import show_data

import signal

yaml_filename = "config/default.yaml"

radar = RadarProcessRunner(yaml_filename)

def sigint_handler(signum, frame):
    radar.stop() # On Ctrl+C, stop the radar process

radar.setup()
radar.run()
signal.signal(signal.SIGINT, sigint_handler)
radar.wait()

file_prefix = radar.stop()

show_data(file_prefix)
