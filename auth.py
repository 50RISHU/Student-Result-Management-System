from utils import generate_hash_pass, check_hash_pass
from models import User
import peewee

def register_user(name, email, roll_no, password, role):
    try:
        hashed_pass = generate_hash_pass(password)
        User.create(name=name, email=email, roll_no= roll_no, password=hashed_pass, role=role)

        message, category, status = "Register Successful", "success", True
        return message, category, status
    
    except peewee.IntegrityError:
        message, category, status = "This email  already exist, try another", "danger", False
        return message, category, status
    

def login_user(email, password):
    user = User.get_or_none(User.email == email)    
    if user:
        if check_hash_pass(user.password, password):
            message, category, status, user = "Login Successful", "success", True, user
            return message, category, status, user
        else:
            message, category, status = "Wrong email or password", "danger", False
            return message, category, status, None
    else:
        return "You Are not regestered", "danger", False, None
