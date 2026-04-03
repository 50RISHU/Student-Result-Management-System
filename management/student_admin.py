from models import User, Subject, Result, ResultItem
from utils import generate_hash_pass

def upload_profile_pic(student:User, filename):
    student.profile_pic = filename
    student.save()
    return "Profile photo uploaded successfully.", "success"

def change_password(student:User, newPass):
    hashesPass = generate_hash_pass(newPass)
    student.password = hashesPass
    student.save()
    return "Password Changed Successfully.", "success"

def change_name(student:User, newName):
    student.name = newName
    student.save()
    return "Name Changed Successfully.", "success"

#  Only for admin
def remove_student(student_id):
    student = User.get_or_none(User.id == student_id, User.role == 'student')
    if not student:
        return "Student not found", "danger", False

    results = Result.select().where(Result.student == student)
    for result in results:
        ResultItem.delete().where(ResultItem.result == result).execute()
        result.delete_instance()

    student.delete_instance()
    return "Student deleted successfully", "success", True

def total_students():
    students = User.select().where(User.role == 'student')
    return students