from flask import Flask, render_template, redirect, request, url_for, session, flash
from auth import register_user, login_user
from functools import wraps
from management.result import add_result, edit_result, delete_result, show_result
from management.subject import add_subject, delete_subject, update_subject
from management.student_admin import total_students, remove_student, upload_profile_pic, change_name, change_password
from models import User, Subject, Result
from datetime import datetime
import uuid
import os

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash('Login Required', 'danger')
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


def admin_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session['role'] != 'admin':
            flash('Only admin can access this page', 'danger')
            return redirect(url_for("dashboard"))
        return func(*args, **kwargs)
    return wrapper


def student_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session['role'] != 'student':
            return redirect(url_for("admin"))
        return func(*args, **kwargs)
    return wrapper



app = Flask(__name__)
app.secret_key = "Students"

UPLOAD_FOLDER = 'static/profile_pic'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_FILES = {'png', 'jpg', 'jpeg', 'gif'}

def isAllowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILES

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        roll_no = request.form['roll_no']
        password = request.form['password']
        role = request.form['role']

        message, category, status = register_user(name=name, email=email, roll_no=roll_no, password=password, role=role)
        flash(message, category)

        if status:
            return redirect(url_for('login'))
        else:
            return redirect(url_for('register')) 

    return render_template('auth/register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        message, category, status, user = login_user(email=email, password=password)
        flash(message = message, category = category)
        if status:
            session['user_id'] = user.id
            
            if user.role == "admin":
                session['role'] = "admin"
                return redirect(url_for('admin'))
            else:
                session['role'] = "student"
                return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))
    return render_template('/auth/login.html')

#  Admin Routes
@app.route('/adminProfile', methods=['GET', 'POST'])
@login_required
@admin_access
def admin_profile():
    user = User.get_by_id(session['user_id'])       

    if request.method == "POST":
        action = request.form.get("action")

        if action == "upload_pfp":
            imagefile = request.files.get("profile_pic")
            if imagefile and isAllowed(imagefile.filename):
                exe = imagefile.filename.rsplit('.', 1)[1].lower()
                filename = str(uuid.uuid4()) + '.' + exe
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagefile.save(filepath)

                message, category = upload_profile_pic(user, filename)
                flash(message, category)
            else:
                flash("Invalid file type", "danger")
            return redirect(url_for('admin'))

        elif action == "change_name":
            newName = request.form.get("name")
            message, category = change_name(user, newName)
            flash(message, category)
            return redirect(url_for('admin'))

        elif action == "change_pass":
            newPass = request.form.get("password")
            message, category = change_password(user, newPass)
            flash(message, category)
            return redirect(url_for('admin'))

    return render_template('admin/adminProfile.html', user=user)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_access
def admin():
    user = User.get_by_id(session['user_id'])
    students = total_students()
    
    return render_template('admin/admin.html', students=students, user = user)

@app.route('/addmark/<int:sid>', methods=['GET', 'POST'])
@login_required
@admin_access
def addmark(sid):
    student = User.get_or_none(User.id == sid)
    subjects = Subject.select()
    
    if not student:
        flash("This student does not exist", "danger")
        return redirect(url_for('admin'))
    
    existing_result = Result.select().where(Result.student == student)
    if existing_result.exists():
        flash("Result already exists for this student.", "warning")
        return redirect(url_for('admin'))

    if request.method == 'POST':
        declaration_date = datetime.now().strftime('%Y-%m-%d')
        marks_data = {}

        for subject in subjects:
            marks_data[str(subject.id)] = {
                'obtained': request.form.get(f'obtained_{subject.id}'),
                'total': request.form.get(f'total_{subject.id}')
            }

        message, category, status = add_result(student.id, declaration_date, marks_data)
        flash(message, category)
        return redirect(url_for('admin'))

    return render_template('admin/addmark.html', student=student, subjects=subjects)


@app.route('/editmark/<int:rid>', methods=['GET', 'POST'])
@login_required
@admin_access
def editmark(rid):
    result = Result.get_or_none(Result.id == rid)
    subjects = Subject.select()
    
    if not result:
        flash("This Resulte id dose not exist", "danger")
        return redirect(url_for('admin'))
    
    items = {item.subject.id: item for item in result.result}

    if request.method == 'POST':
        declaration_date = request.form['declaration_date']
        marks_data = {}

        for subject in subjects:
            marks_data[str(subject.id)] = {
                'obtained': request.form.get(f'obtained_{subject.id}'),
                'total': request.form.get(f'total_{subject.id}')
            }

        message, category, status = edit_result(rid, declaration_date, marks_data)
        flash(message, category)
        return redirect(url_for('admin'))

    return render_template('admin/editmark.html', result=result, items=items, subjects=subjects)


@app.route('/deletemark/<int:rid>', methods=['POST'])
@login_required
@admin_access
def deletemark(rid):
    message, category = delete_result(rid)
    flash(message, category)
    return redirect(url_for('admin'))

@app.route('/allresults')
@login_required
@admin_access
def all_results():
    from models import Result
    results = Result.select().order_by(Result.declaration_date.desc())
    return render_template('admin/allresults.html', results=results)


@app.route('/subject', methods = ['GET', 'POST'])
@login_required
@admin_access
def subject():
    subjects = Subject.select()
    if request.method == "POST":
        sub_name = request.form['sub_name']
        sub_code = request.form['sub_code']
        sub_description = request.form['sub_description']
        
        message, category = add_subject(sub_name=sub_name, sub_code=sub_code, sub_description=sub_description)
        flash(message, category)

        return redirect(url_for('subject'))
        
    return render_template('admin/subject.html', subjects = subjects)

@app.route('/remove_sub/<int:sub_id>', methods = ['GET', 'POST'])
@login_required
@admin_access
def remove_sub(sub_id):
    subject = Subject.get_by_id(sub_id)
    message, category = delete_subject(subject)
    flash(message, category)

    return redirect(url_for('subject'))
    
@app.route('/update_sub/<int:sub_id>', methods = ['GET', 'POST'])
@login_required
@admin_access   
def update_sub(sub_id):
    subject = Subject.get_by_id(sub_id)

    if request.method == "POST":
        sub_name = request.form['sub_name']
        sub_code = request.form['sub_code']
        sub_description = request.form['sub_description']
        
        message, category, status = update_subject(subject, sub_name, sub_code, sub_description)
        flash(message, category)
    
        if status:
            return redirect(url_for('subject'))
        else:
            return redirect(url_for('update_sub', sub_id = subject.id))
        
    return render_template('admin/update_subject.html', subject = subject)
    

@app.route('/remove_std/<int:student_id>', methods=['GET','POST'])
@login_required
@admin_access
def delete_student(student_id):   
    message, category, status = remove_student(student_id)
    flash(message, category)
    return redirect(url_for('admin'))

#  EOF admin routes


#  Student Routes

@app.route('/studentProfile', methods=['GET', 'POST'])
@login_required
@student_access
def student_profile():
    user = User.get_by_id(session['user_id'])
    student = User.get_or_none(User.id == user.id)

    if request.method == "POST":
        action = request.form.get("action")

        if action == "upload_pfp":
            imagefile = request.files.get("profile_pic")
            if imagefile and isAllowed(imagefile.filename):
                exe = imagefile.filename.rsplit('.', 1)[1].lower()
                filename = str(uuid.uuid4()) + '.' + exe
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagefile.save(filepath)

                message, category = upload_profile_pic(student, filename)
                flash(message, category)
            else:
                flash("Invalid file type", "danger")
            return redirect(url_for('dashboard'))

        elif action == "change_name":
            newName = request.form.get("name")
            message, category = change_name(student, newName)
            flash(message, category)
            return redirect(url_for('dashboard'))

        elif action == "change_pass":
            newPass = request.form.get("password")
            message, category = change_password(student, newPass)
            flash(message, category)
            return redirect(url_for('dashboard'))



    return render_template('student/studentProfile.html', student=user)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
@student_access
def dashboard():
    sid = session["user_id"]
    student = User.get_or_none(User.id == sid)
    results = show_result(sid)

    if not student:
        flash("This student does not exist", "danger")
        return redirect(url_for('dashboard'))

    # Calculate percentage
    percentage = 0
    for entry in results:
        total_obtained = sum(float(item.mark_obtain) for item in entry.result)
        total_max = sum(float(item.total_mark) for item in entry.result)
        percentage = round((total_obtained / total_max * 100) if total_max > 0 else 0, 2)

    return render_template("student/dashboard.html", student=student, percentage=percentage, result=results)


@app.route('/myresult')
@login_required
@student_access
def myresult():
    sid = session['user_id']
    results = show_result(sid)
    
    percentage = 0

    for entry in results:
        total_obtained = sum(float(item.mark_obtain) for item in entry.result)
        total_max = sum(float(item.total_mark) for item in entry.result)
        percentage = round((total_obtained / total_max * 100) if total_max > 0 else 0, 2)
    
    return render_template('student/myresult.html', results=results, percentage=percentage)


#  EOF student routes

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contect():
    return render_template('contact.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
