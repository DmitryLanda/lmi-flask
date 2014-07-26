from app import db


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_class = db.relationship('SchoolClass', uselist=False)
    school_class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'))
    day = db.Column(db.String, index=True)
    start_time = db.Column(db.String, index=True)
    end_time = db.Column(db.String, index=True)
    teacher = db.relationship('Teacher', uselist=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    subject = db.relationship('Subject', uselist=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    room = db.relationship('Room', uselist=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))