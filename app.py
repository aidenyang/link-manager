#!flask/bin/python
import os
from flask import Flask, request, jsonify, abort,make_response, request, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
from datetime import timedelta
from functools import update_wrapper

app = Flask(__name__)
heroku = Heroku(app)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b33c15312e395d:ab990249@us-cdbr-east-06.cleardb.net/heroku_493f996d425a69e'

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    url = db.Column(db.Text)
    type = db.Column(db.Integer)
    date_added = db.Column(db.DateTime)

    def __init__(self, title, author, url, type):
        self.title = title
        self.url = url
        self.author = author
        self.type = type

    def __unicode__(self):
        return '<Link %r>' %self.title

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'url': self.url,
            'type': self.type,
            'date_added': self.date_added
        }


@app.route('/links', methods=['GET'])
@crossdomain(origin='*')
def getAllLinks():
    if request.method == 'GET':
        lim = request.args.get('limit', 10)
        off = request.args.get('offset', 0)
        results = Link.query.limit(lim).offset(off).all()

        json_results = []
        for result in results:
            d = {
                    'id': result.id,
                    'title': result.title,
                    'author': result.author,
                    'url': result.url,
                    'type': result.type,
                    'date_added' : result.date_added
                }
            json_results.append(d)
        return jsonify(items=json_results)

@app.route('/links/<int:id>', methods=['GET'])
@crossdomain(origin='*')
def getLinkById(id):
    if request.method == 'GET':
        result = Link.query.filter_by(id=id).first()
        if not result:
            abort(404)
        else:
            json_result = {
            'id': result.id,
            'title': result.title,
            'url': result.url,
            'author': result.author,
            'type': result.type,
            'date_added': result.date_added
            }
            return jsonify(items=json_result)



@app.route('/links', methods=['POST'])
@crossdomain(origin='*')
def postLink():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        author = request.form['author']
        type = request.form['type']
        link = Link(title, url, type)
        db.session.add(link)
        db.session.commit()
        return jsonify({'link' : link.serialize()}), 201


@app.route('/links/<int:id>', methods=['DELETE'])
@crossdomain(origin='*')
def deleteLink(id):
    if request.method == 'DELETE':
        deleted = Link.query.filter(Link.id==id).delete()
        db.session.commit()
        if deleted == 0:
            return "{0} column(s) deleted".format(deleted)
        else:
            return "No columns deleted"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
