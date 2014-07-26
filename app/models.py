from app import db


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    keywords = db.Column(db.String, default='python, flask')
    description = db.Column(db.String, default='Playground for python and flask')
    slug = db.Column(db.String, index=True, unique=True)
    pathname = db.Column(db.String, index=True)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)
    description = db.Column(db.Text)


class SchoolClass(db.Model):
    __tablename__ = "school_class"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)


class Media(db.Model):
    NEWS = 'news'
    TEACHER = 'teacher'
    ROOM = 'room'

    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, index=True)
    type = db.Column(db.String, default=NEWS)
    entity_id = db.Column(db.Integer, index=True)

    @staticmethod
    def create_news_media(news_id, media_api_id):
        return Media(
            entity_id=news_id,
            api_id=media_api_id,
            type='news'
        )