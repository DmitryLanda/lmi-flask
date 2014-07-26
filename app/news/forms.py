# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from models import News
from wtforms import TextAreaField, StringField, HiddenField
from wtforms.validators import Required, ValidationError


class NewsForm(Form):
    id = HiddenField('id')
    title = StringField('name', validators=[Required()])
    body = TextAreaField('about', validators=[Required()])

    def validate_title(self, field):
        news = News.query.filter_by(title=field.data).first()
        if news and int(self.id.data) != news.id:
            raise ValidationError(u'Новость с таким названием уже существует')
