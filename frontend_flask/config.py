import sys
import os

# Some ugly hack to get main app path into sys.path :(
cur_dir = os.path.dirname(os.path.abspath(__file__))
cur_path_wo_last_dir = cur_dir.split(os.sep)[:-1]
path_to_main_app = os.sep.join(cur_path_wo_last_dir)
sys.path.append(path_to_main_app)

DEBUG = True
SECRET_KEY = 'Secret key!'

SQLALCHEMY_DATABASE_URI = 'sqlite:///../daily_stat.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = True
