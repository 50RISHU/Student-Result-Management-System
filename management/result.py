# result.py
from models import User, Subject, Result, ResultItem


def add_result(student_id, declaration_date, marks_data):
    student = User.get_by_id(student_id)
    result = Result.create(student=student, declaration_date=declaration_date)

    for subject_id, marks in marks_data.items():
        subject = Subject.get_by_id(subject_id)
        ResultItem.create(
            result=result,
            subject=subject,
            mark_obtain=marks['obtained'],
            total_mark=marks['total']
        )
    return "Result added successfully", "success", True


def edit_result(result_id, declaration_date, marks_data):
    result = Result.get_by_id(result_id)
    result.declaration_date = declaration_date
    result.save()

    for subject_id, marks in marks_data.items():
        subject = Subject.get_by_id(subject_id)
        item = ResultItem.get(result=result, subject=subject)
        item.mark_obtain = marks['obtained']
        item.total_mark = marks['total']
        item.save()

    return "Result updated successfully", "success", True


def delete_result(result_id):
    result = Result.get_by_id(result_id)
    ResultItem.delete().where(ResultItem.result == result).execute()
    result.delete_instance()
    return "Result deleted successfully", "success"


def show_result(student_id):
    student = User.get_by_id(student_id)
    results = Result.select().where(Result.student == student)
    return results

