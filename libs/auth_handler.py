from . import file_helper
from . import config
from flask import session

import hashlib, binascii, os
 
def login(request):
    users = file_helper.load_json(str(config.DATA_PATH) + "/users.txt")
    user = users.get(request.form.get('username',), {})

    if verify_password(user.get('password'), request.form.get('password')):
        session["USER"] = user.get('username', None)
        return True
        
    return False

def load_user():
    return session.get("USER")

def is_authenticated():
    return "USER" in session

def logout():
    session.pop("USER", None)

def load_all_user():
    users = file_helper.load_json(str(config.DATA_PATH) + "/users.txt")
    return users

def add_user(request):
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
    users = file_helper.load_json(str(config.DATA_PATH) + "/users.txt")
    del users[username]
    file_helper.save_json(str(config.DATA_PATH) + "/users.txt", users)

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
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