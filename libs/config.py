import os
from pathlib import Path

APP_MAIN_PATH = Path(os.path.abspath("/".join(os.path.realpath(__file__).split("/")[:-1])))
DATA_PATH = Path(os.path.abspath(APP_MAIN_PATH/'../data/week_data/'))

UPLOAD_FOLDER = Path(os.path.abspath(APP_MAIN_PATH/'../static/menu_images/'))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

WEEKDAYS_NAME = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
