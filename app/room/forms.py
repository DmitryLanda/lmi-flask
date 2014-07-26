# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from models import Room
from wtforms import TextAreaField, StringField, HiddenField, IntegerField
from wtforms.validators import Required, ValidationError


class RoomForm(Form):
    id = HiddenField('id')
    name = StringField('name', validators=[Required()])
    number = IntegerField('number', validators=[Required()])
    state = TextAreaField('state')

    def validate_name(self, field):
        room = Room.query.filter_by(name=field.data).first()
        if room and int(self.id.data) != room.id:
            raise ValidationError(u'Кабинет с таким названием уже существует')

    def validate_number(self, field):
        room = Room.query.filter_by(number=int(field.data)).first()
        if room and int(self.id.data) != room.id:
            raise ValidationError(u'Кабинет с таким номером уже существует')