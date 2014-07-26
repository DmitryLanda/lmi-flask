from app import db, fotki_manager
from app.models import Media


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)
    birth_date = db.Column(db.DateTime)
    email = db.Column(db.String, index=True, unique=True)
    about = db.Column(db.Text)
    subject = db.relationship('Subject', uselist=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    room = db.relationship('Room', uselist=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    school_class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'))

    def get_album(self):
        """
        Gets teacher related album id and fetches it from cloud
        """
        media = Media.query.filter_by(entity_id=self.id, type=Media.TEACHER).first()

        if not media:
            yield None
        yield fotki_manager.find_album_by_id(media.api_id)

