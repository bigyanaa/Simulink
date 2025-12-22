from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

course_topics = db.Table('course_topics',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'))
)

student_topics = db.Table('student_topics',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
    db.Column('completed', db.Boolean, default=False),
    db.Column('completed_date', db.DateTime, nullable=True)
)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(200), default='default.png')
    
    topics = db.relationship('Topic', 
                           secondary=student_topics,
                           backref='students',
                           lazy='dynamic')
    
    courses = db.relationship('Course', 
                            secondary='student_courses',
                            backref='students')

    def get_completed_topics(self):
        completed = db.session.query(student_topics).filter_by(
            student_id=self.id,
            completed=True
        ).all()
        return [Topic.query.get(t.topic_id) for t in completed]

    def get_course_progress(self, course):
        course_topic_ids = [t.id for t in course.topics]
        completed_topic_ids = [t.id for t in self.get_completed_topics()]
        completed_course_topics = set(course_topic_ids) & set(completed_topic_ids)
        if not course_topic_ids:
            return 0
        return (len(completed_course_topics) / len(course_topic_ids)) * 100

    def get_next_topic(self, course):
        course_topics = course.topics  
        
      
        completed_topics = set(self.get_completed_topics())  

      
        for topic in course_topics:
            if topic not in completed_topics:
                return topic  

        return None  


    def get_recent_topics(self, limit=5):
        recent = db.session.query(Topic).join(
            student_topics,
            Topic.id == student_topics.c.topic_id
        ).filter(
            student_topics.c.student_id == self.id,
            student_topics.c.completed == True
        ).order_by(
            student_topics.c.completed_date.desc()
        ).limit(limit).all()
        return recent

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    topics = db.relationship('Topic', 
                           secondary=course_topics,
                           backref='courses')

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    html_link = db.Column(db.String(200))
    logo_link = db.Column(db.String(200))

    def get_completed_date(self, student_id):
        result = db.session.query(student_topics).filter_by(
            student_id=student_id,
            topic_id=self.id,
            completed=True
        ).first()
        return result.completed_date if result else None

student_courses = db.Table('student_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)