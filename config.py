""" Config file to handle app configurations """
from environs import Env
#Enable Flask's debugging features. Should be False in production.
DEBUG = True
env = Env()
env.read_env()
