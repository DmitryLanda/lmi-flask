# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, flash, redirect, request
from models import Schedule
from app.models import Subject
from app.room.models import Room
from app.teacher.models import Teacher
from forms import ScheduleForm
from app import db
from flask.ext.stormpath import login_required

schedule_module = Blueprint('schedules', __name__, template_folder='templates')
business_days = tuple([u'Понедельник', u'Вторник', u'Среда', u'Четверг', u'Пятница', u'Суббота'])


@schedule_module.route('/')
def list_schedules():
    return render_template('list_schedules.html', schedule_list=Schedule.query.all())


@schedule_module.route('/add', methods=['GET', 'POST'])
@login_required
def add_schedule():
    form = ScheduleForm()
    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]
    form.room.choices = [(r.id, r.name) for r in Room.query.all()]
    form.teacher.choices = [(t.id, t.name) for t in Teacher.query.all()]
    form.day.choices = [(d, d) for d in business_days]

    if form.validate_on_submit():
        schedule = Schedule(
            # school_class_id=form.school_class.data,
            day=form.day.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            teacher_id=form.teacher.data,
            subject_id=form.subject.data,
            room_id=form.room.data
        )

        db.session.add(schedule)
        db.session.commit()

        flash(u'Новая запись успашно добавлена в расписание', 'success')

        return redirect('/schedules/add')

    return render_template('edit_schedule.html', form=form)


@schedule_module.route('/<schedule_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    form = ScheduleForm(request.form, obj=schedule)
    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]
    form.room.choices = [(r.id, r.name) for r in Room.query.all()]
    form.teacher.choices = [(t.id, t.name) for t in Teacher.query.all()]
    form.day.choices = [(d, d) for d in business_days]

    if form.validate_on_submit():
        # schedule.school_class_id = form.school_class.data,
        schedule.day = form.day.data,
        schedule.start_time = form.start_time.data,
        schedule.end_time = form.end_time.data,
        schedule.teacher_id = form.teacher.data,
        schedule.subject_id = form.subject.data,
        schedule.room_id = form.room.data

        db.session.add(schedule)
        db.session.commit()

        flash(u'Расписание успешно обновлено', 'success')

        return redirect('/schedules/')

    return render_template('edit_schedule.html', form=form)