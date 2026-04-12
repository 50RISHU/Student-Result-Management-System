# Student Management System

A Flask-based web application for managing student information, subjects, and academic results. The system provides role-based access control with separate dashboards for administrators and students.

## Features

### General Features
- **User Authentication**: Secure registration and login system with password hashing
- **Role-Based Access Control**: Two user roles - Admin and Student
- **Profile Management**: Upload profile pictures and manage personal information

### Admin Features
- Manage subjects (add, update, delete)
- Manage student results (add, edit, delete)
- View all registered students
- Remove students from the system
- Update student information

### Student Features
- View personal academic results
- Update profile picture
- Change password
- View subject information

## Technology Stack

- **Backend Framework**: Flask 3.1.1
- **Database**: SQLite with Peewee ORM 3.18.1
- **Web Server**: Gunicorn 23.0.0
- **Frontend**: HTML5, CSS3, Bootstrap
- **Language**: Python 3.13+

## Project Structure

```
project/
├── main.py                  # Main Flask application and routes
├── models.py                # Database models (User, Subject, Result, ResultItem)
├── auth.py                  # Authentication functions
├── utils.py                 # Utility functions
├── requirements.txt         # Project dependencies
├── pyproject.toml          # Project configuration
├── management/
│   ├── result.py           # Result management functions
│   ├── subject.py          # Subject management functions
│   └── student_admin.py    # Student administration functions
├── static/
│   ├── profile_pic/        # User profile pictures
│   └── style/
│       └── style.css       # Application stylesheets
└── templates/
    ├── index.html          # Home page
    ├── base.html           # Base template
    ├── about.html          # About page
    ├── contact.html        # Contact page
    ├── auth/
    │   ├── login.html      # Login page
    │   └── register.html   # Registration page
    ├── admin/
    │   ├── admin.html      # Admin dashboard
    │   ├── addmark.html    # Add marks page
    │   ├── editmark.html   # Edit marks page
    │   ├── allresults.html # All results page
    │   ├── subject.html    # Subject management page
    │   └── update_subject.html  # Update subject page
    └── student/
        ├── dashboard.html  # Student dashboard
        └── myresult.html   # Student results page
```


## Usage

### Registration
1. Click on "Register" on the home page
2. Fill in your details (Name, Email, Roll Number, Password)
3. Select your role (Student or Admin)
4. Submit the form

### Login
1. Navigate to the login page
2. Enter your email and password
3. You'll be redirected to the appropriate dashboard based on your role

### Admin Dashboard
- **Manage Subjects**: Add new subjects, view, update, and delete existing subjects
- **Manage Results**: Add marks for students, edit existing marks, delete results
- **Manage Students**: View all students, remove students, upload profile pictures
- **View All Results**: See results for all students

### Student Dashboard
- **View Results**: See your academic results and marks
- **Profile Settings**: 
  - Upload or change profile picture
  - Update your name
  - Change password

## Configuration

The application uses the following configuration:
- **Secret Key**: "Students" (used for session management)
- **Upload Folder**: `static/profile_pic/`
- **Allowed File Types**: PNG, JPG, JPEG, GIF
- **Database**: `student_management.db` (SQLite)


## Security Features

- **Password Hashing**: Passwords are hashed using secure algorithms
- **Session Management**: User sessions are managed securely
- **Role-Based Authorization**: Routes are protected with role-based decorators
- **Input Validation**: Form inputs are validated before processing

## File Upload

- Supported formats: PNG, JPG, JPEG, GIF
- Maximum file size limit enforced
- Files stored in `static/profile_pic/` directory

