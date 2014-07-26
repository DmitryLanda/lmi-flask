# from app import app, db, fotki_manager
# from flask import render_template, abort, jsonify, flash, redirect, request
# from models import Page, Schedule, SchoolClass, Subject, Room
#
#
# @app.route('/static/<slug>.<page_format>')
# @app.route('/static/<slug>')
# def show_page(slug, page_format='html'):
#     page = Page.query.filter_by(slug=slug).first_or_404()
#
#     return render_template('show_page.html', page=page)
#
#
#
#
# @app.route('/fotki')
# def fotki():
#     username = app.config['YA_FOTKI']['username']
#
#     albums = fotki_manager.get_albums(username)
#     # photos = fotki_manager.get_photos(albums.next().links['photos'])
#
#     photo = fotki_manager.find_photo(896335)
#
#     return render_template('fotki.html', photos=[photo])