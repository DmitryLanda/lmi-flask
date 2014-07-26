from app import db, fotki_manager
from app.models import Media


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, index=True, unique=True)
    published = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)
    body = db.Column(db.Text)
    author = db.relationship('Teacher', uselist=False)
    author_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def get_album(self):
        """
        Gets news related album id and fetches it from cloud
        """
        media = Media.query.filter_by(entity_id=self.id, type=Media.NEWS).first()

        if not media:
            yield None
        print 'Found album id - %s' % media.api_id
        yield fotki_manager.find_album_by_id(media.api_id)