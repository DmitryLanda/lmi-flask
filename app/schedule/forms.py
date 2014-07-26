# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, HiddenField, SelectField
from wtforms.validators import Required


class ScheduleForm(Form):
    id = HiddenField('id')
    school_class = StringField('school-class')
    day = SelectField('day', validators=[Required()])
    start_time = StringField('start-time', validators=[Required()])
    end_time = StringField('end-time', validators=[Required()])
    teacher = SelectField('teacher', validators=[Required()], coerce=int)
    subject = SelectField('subject', validators=[Required()], coerce=int)
    room = SelectField('room', validators=[Required()], coerce=int)