__name__ = 'app'

from flask import Flask, render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import jinja2
import logging
from logging.handlers import TimedRotatingFileHandler
from flask.ext.stormpath import StormpathManager
import yafotki
import re

# Init global vars
db = SQLAlchemy()
stormpath_manager = StormpathManager()
file_handler = TimedRotatingFileHandler(filename='logs/log', when='d', backupCount=7)


def create_app():
    global app
    app = Flask(__name__)

    configure_app(app)
    configure_extensions(app)
    configure_blueprints(app)
    configure_logging(app)
    configure_template_filters(app)
    configure_template_extensions(app)
    configure_error_handlers(app)
    configure_start_page(app)

    return app


def configure_app(app):
    app.config.from_object('config')
    app.static_path = app.static_folder


def configure_extensions(app):
    global fotki_manager
    # sqlalchemy
    db.init_app(app)
    # login
    stormpath_manager.init_app(app)
    #Yandex.Fotki

    class FotkiManager(yafotki.Api):
        def find_photo_by_id(self, photo_id):
            """
            Finds photo in Yandex.Fotki storage by given id
            Returns yafotki.Photo object on success and None on failure
            """
            app.logger.debug('Loading photo %d from Yandex.Fotki api' % photo_id)
            url = '/api/users/%s/photo/%d/' % (self.username, photo_id)
            try:
                entry = self._get(url)
                photo = yafotki.Photo(self, entry)
            except AssertionError:
                photo = None

            return photo

        def find_album_by_id(self, album_id):
            """
            Finds album in Yandex.Fotki storage by given id
            Returns yafotki.Album object on success and None on failure
            """
            url = '/api/users/%s/album/%s/' % (self.username, album_id)
            try:
                entry = self._get(url)
                album = yafotki.Album(self, entry)
            except AssertionError:
                album = None

            return album

        def find_album_by_name(self, album_name):
            app.logger.debug('Looking for "%s" album' % album_name)
            albums = self.get_albums(self.username)

            for album in albums:
                if album.title == album_name:
                    return album

            return None

        def create_album(self, title, summary='', parent_link=None, parent=None):
            username = self.username
            title = title or 'Default'
            summary = summary or ''
            data = dict(
                title=yafotki.smart_unicode(title),
                summary=yafotki.smart_unicode(summary)
            )
            if parent_link is not None:
                data['links'] = {'album': self._build_absolute_url(parent_link)}
            elif parent is not None:
                album_url = re.sub('^(.+)/api/', '/api/', parent.links.self)
                album_url = re.sub('\?(.+)$', '', album_url)
                data['links'] = {'album': album_url}
            url = '/api/users/%s/albums/' % username

            entry = self._post(
                url,
                data=data
            )

            return yafotki.Album(self, entry)

    fotki_manager = FotkiManager(app.config['YA_FOTKI']['app_id'], app.config['YA_FOTKI']['app_key'])
    fotki_manager.auth(app.config['YA_FOTKI']['username'], app.config['YA_FOTKI']['password'])


def configure_blueprints(app):
    from teacher.views import teacher_module
    app.register_blueprint(teacher_module, url_prefix='/teachers')

    from news.views import news_module
    app.register_blueprint(news_module, url_prefix='/news')

    from room.views import room_module
    app.register_blueprint(room_module, url_prefix='/rooms')

    from schedule.views import schedule_module
    app.register_blueprint(schedule_module, url_prefix='/schedules')


def configure_template_filters(app):
    # @app.template_filter()
    # def pretty_date(value):
    #     return utils.pretty_date(value)
    pass


def configure_template_extensions(app):
    @app.context_processor
    def init_template_extensions():
        def include_raw(filename, src_dir=None):
            if not src_dir:
                src_dir = app.config['STATIC_PAGES_DIR']
            loader = jinja2.PackageLoader(__name__, src_dir)
            env = jinja2.Environment(loader=loader)

            return jinja2.Markup(loader.get_source(env, filename)[0])
        return dict(include_raw=include_raw)


def configure_logging(app):
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)


def configure_error_handlers(app):

    # @app.errorhandler(403)
    # def forbidden_page(error):
    #     return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    # @app.errorhandler(405)
    # def method_not_allowed_page(error):
    #     return render_template("errors/method_not_allowed.html"), 405

    # @app.errorhandler(500)
    # def server_error_page(error):
    #     return render_template("errors/server_error.html"), 500


def configure_start_page(app):
    @app.route('/')
    def start_page():
        return redirect(url_for('news.list_news'))

app = create_app()

from app import views, models
