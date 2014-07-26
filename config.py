import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

STATIC_PAGES_DIR = 'static/pages'

STORMPATH_API_KEY_FILE = os.path.join(basedir, 'apiKey.properties')
STORMPATH_APPLICATION = 'lmi-school'
STORMPATH_ENABLE_REGISTRATION = False
STORMPATH_LOGIN_TEMPLATE = 'stormpath/login.html'

LESS_PATH = os.path.join(basedir, 'app/static/less')

UPLOAD_FOLDER = os.path.join(basedir, 'tmp/uploads')

YA_FOTKI = {
    'app_id': 'fe9e6950f95a42cf8a390b6cf382de7a',
    'app_key': '8cf005f4aa3b4c3c800ebe3468026b1c',
    'username': 'lmi-images',
    'password': 'lmi113',
    'news_album_link': '/api/users/lmi-images/album/438055/',
    'teachers_album_link': '/api/users/lmi-images/album/367805/',
    'rooms_album_link': '/api/users/lmi-images/album/438299/'

}