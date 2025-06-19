from models import User, Subject, Result, ResultItem
import peewee


def add_subject(sub_name, sub_code, sub_description):
    try:
        Subject.create(sub_name=sub_name, sub_code=sub_code, sub_description=sub_description)
        message, category = "Subject Add Successful", "success"
        return message, category
    except peewee.IntegrityError:
        message, category = "This subject code already exist", "danger"    
        return message, category


def delete_subject(subject:Subject):
    subject.delete_instance()
    
    return "Subject deleted successfully.", "success"
    

def update_subject(subject:Subject, sub_name, sub_code, sub_description):
    try:
        subject.sub_name = sub_name
        subject.sub_code = sub_code
        subject.sub_description = sub_description
        subject.save()
        
        message, category, status = "Subject Updated Successfully.", "success", True
        return message, category, status
    
    except peewee.IntegrityError:
        
        message, category, status = "Subject Can't Update.", "danger", False
        return message, category, status