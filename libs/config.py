import os
from pathlib import Path

app_main_path = Path(os.path.abspath("/".join(os.path.realpath(__file__).split("/")[:-1])))
data_path = Path(os.path.abspath(app_main_path/'../week_data/'))

