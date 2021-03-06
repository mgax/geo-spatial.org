#!/usr/bin/env python

import sys
import subprocess
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Article(Base):
    __tablename__ = 'txp_textpattern'

    id = Column(Integer, primary_key=True)
    posted = Column(DateTime)
    authorid = Column(String)
    title = Column(String)
    body_html = Column(String)
    excerpt = Column(String)
    category1 = Column(String)
    category2 = Column(String)
    section = Column(String)
    url_title = Column(String)


class User(Base):
    __tablename__ = 'site_users'

    id = Column(Integer, primary_key=True)
    userid = Column(String)
    name = Column(String)
    website = Column(String)
    description = Column(String)
    photo = Column(String)
    signupdate = Column(DateTime)


def create_session(dbname):
    engine = create_engine('mysql+oursql://root@localhost/' + dbname)
    return sessionmaker(bind=engine)()


def jsonify(txt):
    return json.dumps(txt, ensure_ascii=False).encode('utf-8')


def export(slug):
    article = session.query(Article).filter_by(url_title=slug).one()
    html = (
        article.body_html
        .replace('http://www.geo-spatial.org/images',
                 '{{ site.image_base_url }}')
        .replace('http://www.geo-spatial.org',
                 '{{ site.base_url }}')
    )
    folder = '_' + article.section
    with open(folder + '/' + slug + '.html', 'wb') as f:
        f.write('---\n')
        f.write('title: ' + jsonify(article.title) + '\n')
        f.write('authorid: ' + jsonify(article.authorid) + '\n')
        f.write('excerpt: ' + jsonify(article.excerpt) + '\n')
        f.write('category1: ' + jsonify(article.category1) + '\n')
        f.write('category2: ' + jsonify(article.category2) + '\n')
        f.write('time: ' + str(article.posted) + '\n')
        f.write('---\n')
        f.write(html.replace('\r\n', '\n').encode('utf-8'))
        f.write('\n')


def dump_authors():
    for user in session.query(User).order_by('id'):
        if user.userid == '57': user.userid = 'alex'
        with open('_autori/' + user.userid + '.html', 'wb') as f:
            f.write('---\n')
            f.write('slug: ' + user.userid.encode('utf-8') + '\n')
            f.write('name: ' + user.name.encode('utf-8') + '\n')
            f.write('photo: ' + user.photo.encode('utf-8') + '\n')
            f.write('signup_date: ' + str(user.signupdate) + '\n')
            f.write('order: ' + str(user.id) + '\n')
            f.write('---\n')
            f.write(user.description.encode('utf-8'))
            f.write('\n')


TEST_NAMES = [
    'adaugarea-i-editarea-datelor-in-openstreetmap-folosind-josm-func-ii-avansate',
    'doilasuta2013',
    'georeferentierea-imaginilor-satelitare-google-folosind-qgis-si-josm',
    'habsburg-google-earth',
    'hartile-sovietice-50k',
    'porto-franco-sulina',
    'preluarea-datelor-din-openstreetmap-folosind-overpass',
]


arg = sys.argv[1]

if arg == '--users':
    session = create_session('earth')
    dump_authors()
else:
    session = create_session('geospatial')
    if arg == '--test':
        for name in TEST_NAMES:
            print name
            export(name)
    else:
        export(arg)
