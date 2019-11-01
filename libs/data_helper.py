import os.path
import json

from . import config
from werkzeug.utils import secure_filename

def file_exists(file_path):
    """Summary
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
    """Summary
    Args:
        json_path (String): Path to file
        data (String): String to save
    """
    with open(json_path, "w", encoding="utf-8") as open_file:
        json.dump(data, open_file, indent=4)

def load_json(json_path):
    """Summary
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
    if 'file' not in request.files:
        print("file not found")
    file = request.files['file']
    if file.filename == '':
	    print('No file selected for uploading')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(config.UPLOAD_FOLDER, filename))
        print('File successfully uploaded')
        return filename
    else:
        print('Allowed file types are txt, pdf, png, jpg, jpeg, gif') 
	

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

