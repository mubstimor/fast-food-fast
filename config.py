""" Config file to handle app configurations """
# import os
from environs import Env

#Enable Flask's debugging features. Should be False in production.
DEBUG = True
env = Env()
env.read_env()

# class BaseConfig:
#     """Base configuration"""
#     TESTING = False
#     TRACK_MODIFICATIONS = False 

# class DevelopmentConfig(BaseConfig):
#     """Development configuration"""
#     DATABASE_URI = env.str("DATABASE_URL")

# class TestingConfig(BaseConfig):
#     """Testing configuration"""
#     TESTING = True
#     DATABASE_URI = env.str('DATABASE_TEST_URL')  

# class ProductionConfig(BaseConfig):
#     """Production configuration"""
#     DATABASE_URI = env.str('DATABASE_URL') 