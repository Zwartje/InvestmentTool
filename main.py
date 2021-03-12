# This is a sample Python script.

from configparser import ConfigParser, ExtendedInterpolation

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('configuration.ini')

root_folder = config['general']['root_folder']
test_extension = config['general']['test_extension']

