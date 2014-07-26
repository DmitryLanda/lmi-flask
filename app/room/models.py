from app import db, fotki_manager
from app.models import Media


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    number = db.Column(db.Integer, index=True)
    state = db.Column(db.Text)

    def get_album(self):
        """
        Gets news related album id and fetches it from cloud
        """
        media = Media.query.filter_by(entity_id=self.id, type=Media.ROOM).first()

        if not media:
            yield None
        yield fotki_manager.find_album_by_id(media.api_id)