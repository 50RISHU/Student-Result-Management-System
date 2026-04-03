from peewee import *

db = SqliteDatabase("student_management.db")

class BaseClass(Model):
    class Meta:
        database = db

class User(BaseClass):
    name = CharField()
    email = CharField(unique = True)
    roll_no = CharField(unique = True)
    profile_pic = CharField(default="")
    password = CharField()
    role = CharField(default="student")

class Subject(BaseClass):
    sub_code = CharField(unique = True)
    sub_name = CharField()
    sub_description = TextField()

class Result(BaseClass):
    student = ForeignKeyField(User, backref='student')
    declaration_date = CharField()

class ResultItem(BaseClass):
    result = ForeignKeyField(Result, backref='result')
    subject = ForeignKeyField(Subject, backref='subject')
    mark_obtain = CharField()
    total_mark = CharField()


# db.connect()
# db.create_tables([User, Subject, Result, ResultItem])    