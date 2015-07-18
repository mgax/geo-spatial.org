#!/usr/bin/env python

import sys
import subprocess
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+oursql://root@localhost/geospatial')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Article(Base):
    __tablename__ = 'txp_textpattern'

    id = Column(Integer, primary_key=True)
    posted = Column(DateTime)
    authorid = Column(String)
    title = Column(String)
    body_html = Column(String)
    url_title = Column(String)


session = Session()


def export(slug):
    article = session.query(Article).filter_by(url_title=slug).one()
    print article.body_html
    with open('article/' + slug + '.html', 'wb') as f:
        f.write('---\n')
        f.write('title: ' + json.dumps(article.title) + '\n')
        f.write('authorid: ' + json.dumps(article.authorid) + '\n')
        f.write('---\n')
        f.write(article.body_html.encode('utf-8'))


export(sys.argv[1])
