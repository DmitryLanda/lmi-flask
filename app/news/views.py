# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, flash, redirect, request
from models import News
from app.models import Media
from forms import NewsForm
from app import app, db, fotki_manager
from flask.ext.stormpath import login_required
from datetime import datetime
from hashlib import md5
from time import time
import os

news_module = Blueprint('news', __name__, template_folder='templates')


def pre_upload_files(request_files):
    files = {}
    m = md5()
    for news_image in request_files:
        m.update(news_image.filename + str(time()))
        filename = m.hexdigest()
        url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        files[news_image.filename] = url
        news_image.save(url)

    return files


def add_files_to_storage(files, news):
    album = news.get_album()
    album = album.next()

    if album is None:
        album = fotki_manager.create_album(
            title='%s (%s)' % (news.title, news.last_modified.strftime('%d %m %Y')),
            parent_link=app.config['YA_FOTKI']['news_album_link']
        )
        print 'Album %s created' % album.id

    for filename in files.keys():
        filepath = files[filename]
        fotki_manager.upload(
            album,
            filepath,
            title=filename,
            tags=u'новости,лми,%s,%s' % (news.title, news.last_modified.strftime('%Y'))
        )

    db.session.add(Media(api_id=album.id, entity_id=news.id, type=Media.NEWS))
    db.session.commit()


@news_module.route('/')
def list_news():
    return render_template('list_news.html', news_list=News.query.all())


@news_module.route('/<news_id>')
def show_news(news_id):
    return render_template('show_news.html', news=News.query.get_or_404(news_id))


def clear_preloaded_files(files):
    for filename in files.values():
        os.remove(filename)


@news_module.route('/add', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    files = {}

    if request.method == 'POST' and request.files:
        files = pre_upload_files(request.files.getlist('news_files[]'))

    if form.validate_on_submit():
        news = News(
            title=form.title.data,
            body=form.body.data,
            published=datetime.now(),
            last_modified=datetime.now()
        )

        db.session.add(news)
        db.session.commit()

        try:
            add_files_to_storage(files, news)
            flash(u'Новость успешно добавлена', 'success')
        except Exception as e:
            app.logger.error(e)
            flash(u'Новость не добавлена', 'error')
        finally:
            clear_preloaded_files(files)

        return redirect('/news/add')

    clear_preloaded_files(files)

    return render_template('edit_news.html', form=form)


@news_module.route('/<news_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    news = News.query.get_or_404(news_id)
    form = NewsForm(request.form, obj=news)
    files = {}

    if request.method == 'POST' and request.files:
        files = pre_upload_files(request.files.getlist('news_files[]'))

    if form.validate_on_submit():
        news.title = form.title.data
        news.body = form.body.data
        news.last_modified = datetime.now()

        db.session.add(news)
        db.session.commit()

        try:
            add_files_to_storage(files, news)
            flash(u'Новость успешно добавлена', 'success')
        except Exception as e:
            app.logger.error(e)
            flash(u'Новость не добавлена', 'error')
        finally:
            clear_preloaded_files(files)

        return redirect('/news/')

    clear_preloaded_files(files)

    return render_template('edit_news.html', form=form)