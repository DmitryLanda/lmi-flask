# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, flash, redirect, request
from models import Room
from app.models import Media
from forms import RoomForm
from app import app, db, fotki_manager
from flask.ext.stormpath import login_required
from datetime import datetime
from hashlib import md5
from time import time
import os

room_module = Blueprint('rooms', __name__, template_folder='templates')


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
            title='%s.%s' % (entity.number, entity.name),
            parent_link=app.config['YA_FOTKI']['rooms_album_link']
        )

    for filename in files.keys():
        filepath = files[filename]
        fotki_manager.upload(
            album,
            filepath,
            title=filename,
            tags=u'кабинеты,лми,кабинет № %s,%s' % (entity.number, entity.name)
        )

    db.session.add(Media(api_id=album.id, entity_id=entity.id, type=Media.ROOM))
    db.session.commit()


def _clear_preloaded_files(files):
    for filename in files.values():
        os.remove(filename)


@room_module.route('/')
def list_rooms():
    return render_template('list_rooms.html', room_list=Room.query.all())


@room_module.route('/<room_number>')
def show_room(room_number):
    return render_template('show_room.html', room=Room.query.filter_by(number=room_number).first_or_404())


@room_module.route('/add', methods=['GET', 'POST'])
@login_required
def add_room():
    form = RoomForm()
    files = {}

    if request.method == 'POST' and request.files:
        files = _pre_upload_files(request.files.getlist('room_files[]'))

    if form.validate_on_submit():
        room = Room(
            name=form.name.data,
            number=int(form.number.data),
            state=form.state.data
        )

        db.session.add(room)
        db.session.commit()

        try:
            _add_files_to_storage(files, room)
            flash(u'Новый кабинет успешно добавлен', 'success')
        except Exception as e:
            app.logger.error(e)
            flash(u'Произошла ошибка при добавлении кабинета', 'error')
        finally:
            _clear_preloaded_files(files)

        return redirect('/rooms/add')

    _clear_preloaded_files(files)

    return render_template('edit_room.html', form=form)


@room_module.route('/<room_number>/edit', methods=['GET', 'POST'])
@login_required
def edit_room(room_number):
    room = Room.query.filter_by(number=room_number).first_or_404()
    form = RoomForm(request.form, obj=room)
    files = {}

    if request.method == 'POST' and request.files:
        files = _pre_upload_files(request.files.getlist('room_files[]'))

    if form.validate_on_submit():
        room.name = form.name.data
        room.number = form.number.data
        room.state = form.state.data

        db.session.add(room)
        db.session.commit()

        try:
            _add_files_to_storage(files, room)
            flash(u'Кабинет успешно изменен', 'success')
        except Exception as e:
            app.logger.error(e)
            flash(u'Произошла ошибка, кабинет не может быть изменен', 'error')
        finally:
            _clear_preloaded_files(files)

        return redirect('/rooms/')

    _clear_preloaded_files(files)

    return render_template('edit_room.html', form=form)