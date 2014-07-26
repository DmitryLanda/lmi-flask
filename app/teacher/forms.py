# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from models import Teacher
from wtforms import DateField, SelectField, TextAreaField, StringField
from wtforms.validators import Required, Email, ValidationError


class TeacherForm(Form):
    name = StringField('name', validators=[Required()])
    birth_date = DateField('birth_date', validators=[Required()])
    email = StringField('email', validators=[Required(), Email()])
    about = TextAreaField('about')
    subject = SelectField('subject', validators=[Required()], coerce=int)
    room = SelectField('room', coerce=int)
    school_class = SelectField('school_class', coerce=int)

    def validate_name(self, field):
        if Teacher.query.filter_by(name=field.data).first():
            raise ValidationError(u'Учитель с таким именем уже существует')

    def validate_email(self, field):
        if Teacher.query.filter_by(email=field.data).first():
            raise ValidationError(u'Адрес электронной почты уже используется')