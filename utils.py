from werkzeug.security import generate_password_hash, check_password_hash

def generate_hash_pass(password):
    hash_pass = generate_password_hash(password)
    return hash_pass

def check_hash_pass(hash_pass, password):
    status = check_password_hash(hash_pass, password)
    if status:
        return status
    else:
        return False