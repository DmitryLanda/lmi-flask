# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, flash, redirect, request
from models import Teacher
from app.models import Media, Subject, SchoolClass
from forms import TeacherForm
from app.room.models import Room
from app import app, db, fotki_manager
from flask.ext.stormpath import login_required
from hashlib import md5
from time import time
import os

teacher_module = Blueprint('teachers', __name__, template_folder='templates')


def _pre_upload_files(request_files):
    files = {}
    m = md5()
    for news_image in request_files:
        m.update(news_image.filename + str(time()))
        filename = m.hexdigest()
        url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        files[news_image.filename] = url
        news_image.save(url)

    return files


def _add_files_to_storage(files, entity):
    album = entity.get_album()
    album = album.next()

    if album is None:
        album = fotki_manager.create_album(
            title='%s' % entity.name,
            parent_link=app.config['YA_FOTKI']['teachers_album_link']
        )

    for filename in files.keys():
        filepath = files[filename]
        fotki_manager.upload(
            album,
            filepath,
            title=filename,
            tags=u'кабинеты,лми,учителя,%s' % entity.name
        )

    db.session.add(Media(api_id=album.id, entity_id=entity.id, type=Media.TEACHER))
    db.session.commit()


def _clear_preloaded_files(files):
    for filename in files.values():
        os.remove(filename)


@teacher_module.route('/')
def list_teachers():
    return render_template('list_teachers.html', teacher_list=Teacher.query.all())


@teacher_module.route('/<teacher_id>')
def show_teacher(teacher_id):
    return render_template('show_teacher.html', teacher=Teacher.query.get_or_404(teacher_id))


@teacher_module.route('/add', methods=['GET', 'POST'])
@login_required
def add_teacher():
    form = TeacherForm()
    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]
    form.room.choices = [(r.id, r.name) for r in Room.query.all()]
    form.room.choices.insert(1, (17, 17))
    form.school_class.choices = [(c.id, c.name) for c in SchoolClass.query.all()]
    files = {}

    if request.method == 'POST' and request.files:
        files = _pre_upload_files(request.files.getlist('teacher_files[]'))

    if form.validate_on_submit():
        teacher = Teacher(
            name=form.name.data,
            birth_date=form.birth_date.data,
            email=form.email.data,
            about=form.about.data,
            subject_id=form.subject.data,
            room_id=form.room.data or 17,
            school_class_id=form.school_class.data
        )

        db.session.add(teacher)
        db.session.commit()

        try:
            _add_files_to_storage(files, teacher)
            flash(u'Учитель %s успешно добавлен' % teacher.name, 'success')
        except Exception as e:
            app.logger.error(e)
            flash(u'Произошла ошибка при добавлении учителя', 'error')
        finally:
            _clear_preloaded_files(files)

        return redirect('/teachers')

    _clear_preloaded_files(files)

    return render_template('edit_teacher.html', form=form)


@teacher_module.route('/<teacher_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    form = TeacherForm(request.form, obj=teacher)
    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]
    form.room.choices = [(r.id, r.name) for r in Room.query.all()]
    form.room.choices.insert(0, ('', ''))
    form.school_class.choices = [(c.id, c.name) for c in SchoolClass.query.all()]
    files = {}

    if request.method == 'POST' and request.files:
        files = _pre_upload_files(request.files.getlist('teacher_files[]'))

    if form.validate_on_submit():
        teacher.name = form.name.data
        teacher.birth_date = form.birth_date.data
        teacher.email = form.email.data
        teacher.about = form.about.data
        teacher.room_id = form.room.data or 17,
        teacher.subject_id = form.subject.data,
        teacher.school_class_id = form.school_class.data

        db.session.add(teacher)
        db.session.commit()

        try:
            _add_files_to_storage(files, teacher)
            flash(u'Учитель %s успешно изменен' % teacher.name, 'success')
        except Exception as e:
            app.logger.error(e)
            flash(u'Произошла ошибка, невозможно изменить данные учителя', 'error')
        finally:
            _clear_preloaded_files(files)

        return redirect('/teachers/')

    _clear_preloaded_files(files)

    return render_template('edit_teacher.html', form=form)