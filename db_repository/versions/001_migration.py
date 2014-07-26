# -*- coding: utf-8 -*-

from sqlalchemy import *
from migrate import *
from migrate.changeset import schema

pre_meta = MetaData()
post_meta = MetaData()

subject = Table('subject', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('description', String)
)
school_class = Table('school_class', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String)
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine

    connection = post_meta.bind.connect()

    connection.execute(subject.insert(), [
        {'name': u'Математика', 'description': u'Математика'},
        {'name': u'Русский язык', 'description': u'Русский язык'},
        {'name': u'Литература', 'description': u'Литература'},
        {'name': u'История', 'description': u'История'},
        {'name': u'Информатика', 'description': u'Информатика'},
        {'name': u'Химия', 'description': u'Химия'},
        {'name': u'Физика', 'description': u'Физика'},
        {'name': u'Физическая культура', 'description': u'физическая культура'}
    ])
    connection.execute(school_class.insert(), [
        {'name': '2-1'},
        {'name': '3-1'},
        {'name': '5-1'},
        {'name': '5-2'},
        {'name': '6-1'},
        {'name': '6-2'},
        {'name': '7-1'},
        {'name': '7-2'},
        {'name': '7-3'}
    ])


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine

    connection = pre_meta.bind.connect()

    connection.execute(subject.delete())
    connection.execute(school_class.delete())
