import os.path
import json

from . import config
from werkzeug.utils import secure_filename

def file_exists(file_path):
    """Summary Checks if a file exists
    Args:
        file_path (String): Path to file
    Returns:
        boolean: Checks if a file exists
    """
    if (os.path.exists(file_path) and os.path.isfile(file_path)):
        return True
    else:
        return False

def save_json(json_path, data):
    """Summary saves a json to a file
    Args:
        json_path (String): Path to file
        data (String): String to save
    """
    with open(json_path, "w", encoding="utf-8") as open_file:
        json.dump(data, open_file, indent=4)

def load_json(json_path):
    """Summary load a json from a file
    Args:
        json_path (String): Path to file
    Returns:
        String: Content of file
    """
    print(json_path)
    data = {}
    try:
        with open(json_path, "r") as open_file:
            data = json.load(open_file)
    except:
        print("Error with file at", json_path, "!")
    finally:
        return data

def upload_image(request):
    """Saves a image to the file system
    Args:
        request (Request): Form request
    Returns:
        String: Filename of the save file
    """
    if 'file' not in request.files:
        print("file not found")
    else:
        file = request.files['file']
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(config.UPLOAD_FOLDER, filename))
            return filename
	
def allowed_file(filename):
    """Checks if the file type is allowed in the application
    Returns:
        Boolean: File type allowed
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def read_all_weeks():
    path = str(config.DATA_PATH) + '/week_data/'
    data = []
    for filename in os.listdir(path):
        file_path = '%s%s%s' % (config.DATA_PATH, '/week_data/' , filename)
        data.append(load_json(file_path))

    return data


