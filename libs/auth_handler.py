from . import file_helper
from . import config
from flask import session

import hashlib, binascii, os
 
def login(request):
    """Summary:
        Checks if the file type is allowed in the application
    Args:
        Request: The request of the page login.html
    Returns:
        Boolean: If user successfully logged in
    """
    users = file_helper.load_json(str(config.DATA_PATH) + "/users.txt")
    user = users.get(request.form.get('username',), {})

    if verify_password(user.get('password'), request.form.get('password')):
        session["USER"] = user.get('username', None)
        return True
        
    return False

def load_user():
    """Summary:
        Loads the user from the session
    Returns:
        String: Username of the logged in user
    """
    return session.get("USER")

def is_authenticated():
    """Summary:
        Checks if a user is logged in
    Returns:
        Boolean: True if a user is authenticated
    """
    return "USER" in session

def logout():
    """Summary:
        Logs a user out and delete it from session
    """
    session.pop("USER", None)

def load_all_user():
    """Summary:
        Loads all users that exists from file
    Returns:
        Dict: All users from file
    """
    users = file_helper.load_json(str(config.DATA_PATH) + "/users.txt")
    return users

def add_user(request):
    """Summary:
        Adds a user to the system
    Args:
        Request: The request of the page manage_user.html
    """
    request_form = request.form
    users = file_helper.load_json(str(config.DATA_PATH) + "/users.txt")

    users[request_form.get('username')] = {
        'username': request_form.get('username'), 
        'password': hash_password(request_form.get('password')), 
        'firstname': request_form.get('firstname'), 
        'lastname': request_form.get('lastname'),
        'roles': request_form.getlist('checkbox')
    }
    file_helper.save_json(str(config.DATA_PATH) + "/users.txt", users)

def delete_user(username):
    """Summary:
        Deletes a user from the system
    Args:
        String: Username of user to delete
    """
    users = file_helper.load_json(str(config.DATA_PATH) + "/users.txt")
    del users[username]
    file_helper.save_json(str(config.DATA_PATH) + "/users.txt", users)

def hash_password(password):
    """Summary:
        Hash a password for storing.
    Args:
        String: Plaintext password
    Returns:
        String: Secured password
    """
    # Quelle: https://www.vitoshacademy.com/hashing-passwords-in-python/
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii') 
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Summary:
        Verify a stored password against one provided by user
    Args:
        String: Plaintext password from form
        String: Plaintext password from data
    Returns:
        Boolean: If two args are the same
    """
    # Quelle: https://www.vitoshacademy.com/hashing-passwords-in-python/
    pwdhash = ""
    if stored_password:
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                    provided_password.encode('utf-8'), 
                                    salt.encode('ascii'), 
                                    100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        pwdhash == stored_password
    return pwdhash 