from flask import Flask, render_template,request,redirect,url_for
from models import db, Student, Course, Topic, student_topics
from datetime import datetime
import random
from ai_config import modifyAccordingToParameter
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/paraphraseAndSubmit', methods=['POST'])
def paraphraseAndSubmit():
    gottenValue = request.form
    print(gottenValue.to_dict())
    toSend = render_template(gottenValue.to_dict()['destination'])
    
    
    soup = BeautifulSoup((toSend), 'html.parser')
    for tag in soup.find_all(class_= "tochange"):
        tag.string = modifyAccordingToParameter(tag.get_text(),gottenValue.to_dict())
    return str(soup)

@app.route('/continue/')
def continue_():
    student = Student.query.first()
    course = student.courses[0] if student.courses else None
    next_topic = student.get_next_topic(course)
    if next_topic:
        db.session.execute(student_topics.insert().values(
            student_id=student.id,
            topic_id=next_topic.id,
            completed=True,
            completed_date=datetime.now()
        ))
        print("DONE")
    
    db.session.commit()

    return redirect(url_for('index'))
    

@app.route('/<page_name>')
def page(page_name):
    allowed_pages_main = Topic.query.all()

    allowed_pages = [page.html_link for page in allowed_pages_main]
    allowed_pages_name = [page2.name for page2 in allowed_pages_main]
    allowed_pages_id = [page3.id for page3 in allowed_pages_main]
    if page_name in allowed_pages:
        return render_template('questionaire.html',pageId=allowed_pages_id[allowed_pages.index(page_name)], destination=page_name,name=allowed_pages_name[allowed_pages.index(page_name)])
    return render_template(page_name)

@app.route('/')
def index():
    student = Student.query.first()
    if not student:
        return "No student found"
    
    course = student.courses[0] if student.courses else None
    if not course:
        return "No course found"
    
    progress = student.get_course_progress(course)
    recent_topics = student.get_recent_topics()
    
    return render_template('index.html',
        profilePic = "ram.jpg",
        student=student,
        course=course,
        progress=progress,
        recent_topics=recent_topics,
        next_topic=(student.get_next_topic(course).html_link if student.get_next_topic(course)!=None else "Completed" )
    )

def add_random_data():
    topics = [
        Topic(name='Python Basics', html_link='python.html', logo_link='python.png'),
        Topic(name='Variables', html_link='variables.html', logo_link='vars.png'),
        Topic(name='Functions', html_link='functions.html', logo_link='func.png'),
        Topic(name='Classes', html_link='classes.html', logo_link='class.png')
    ]
    for topic in topics:
        db.session.add(topic)
    
    course = Course(name='Python Programming')
    course.topics = topics
    db.session.add(course)
    
    student = Student(
        name='John Doe',
        profile_pic='john.png'
    )
    student.courses = [course]
    db.session.add(student)
    
    db.session.commit()
    
    completed_topics = random.sample(topics, 2)
    for topic in completed_topics:
        db.session.execute(student_topics.insert().values(
            student_id=student.id,
            topic_id=topic.id,
            completed=True,
            completed_date=datetime.now()
        ))
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Student.query.first():
            add_random_data()
    app.run(debug=True)