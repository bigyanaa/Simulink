from models import db, Student, Course, Topic
import random

def add_random_data():
    # Sample data
    topic_data = [
        {'name': 'Python', 'html_link': 'python.html', 'logo_link': 'python.png'},
        {'name': 'JavaScript', 'html_link': 'js.html', 'logo_link': 'js.png'},
        {'name': 'Database', 'html_link': 'db.html', 'logo_link': 'db.png'}
    ]
    
    course_names = ['Web Development', 'Programming Basics', 'Data Science']
    student_names = ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown']

    # Add topics
    topics = []
    for t_data in topic_data:
        topic = Topic(**t_data)
        db.session.add(topic)
        topics.append(topic)

    # Add courses
    courses = []
    for name in course_names:
        course = Course(name=name)
        course.topics = random.sample(topics, random.randint(1, 3))
        db.session.add(course)
        courses.append(course)

    # Add students
    for name in student_names:
        student = Student(name=name)
        student.courses = random.sample(courses, random.randint(1, 2))
        db.session.add(student)

    db.session.commit()