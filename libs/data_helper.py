import os.path
import json

def file_exists(file_path):
    if (os.path.exists(file_path) and os.path.isfile(file_path)):
        return True
    else:
        return False

def save_json(json_path, data):
    with open(json_path, "w", encoding="utf-8") as open_file:
        json.dump(data, open_file, indent=4)

def load_json(json_path):
    print(json_path)
    data = {}
    try:
        with open(json_path, "r") as open_file:
            data = json.load(open_file)
    except:
        print("Error with file at", json_path, "!")
    finally:
        return data