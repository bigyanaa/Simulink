from flask import Flask, jsonify
from models import db, Student, Course, Topic
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/add_random_student', methods=['POST'])
def add_random_student():
    courses = Course.query.all()
    if not courses:
        return jsonify({'message': 'No courses available to enroll in.'}), 400

    course = random.choice(courses)
    
    student_name = f"Student {random.randint(1, 100)}" 
    student = Student(name=student_name, course_id=course.id)

    db.session.add(student)
    db.session.commit()
    
    return jsonify({'message': f'Student {student_name} enrolled in {course.name} successfully.'})

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    student_list = [{'id': student.id, 'name': student.name, 'course': student.course.name} for student in students]
    return jsonify(student_list)

if __name__ == '__main__':
    app.run(debug=True)
