#!flask/bin/python
import os
from flask import Flask, request, jsonify, abort, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
from cors import crossdomain

app = Flask(__name__)
app.debug = True
heroku = Heroku(app)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b33c15312e395d:ab990249@us-cdbr-east-06.cleardb.net/heroku_493f996d425a69e'

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

# Todo: Get by media type, get by time period, get by 
@app.route('/links', methods=['GET'])
@crossdomain(origin='*', headers='Content-Type')
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
@crossdomain(origin='*', headers='Content-Type')
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
@crossdomain(origin='*', headers='Content-Type')
def postLink():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        author = request.form['author']
        type = request.form['type']
        link = Link(title, author, url, type)
        db.session.add(link)
        db.session.commit()
        return jsonify({'link' : link.serialize()}), 201


@app.route('/links/<int:id>', methods=['DELETE'])
@crossdomain(origin='*', headers='Content-Type')
def deleteLink(id):
    if request.method == 'DELETE':
        deleted = Link.query.filter(Link.id==id).delete()
        db.session.commit()
        if deleted == 0:
            return "{0} column(s) deleted".format(deleted)
        else:
            return "No columns deleted"


@app.route('/mylinks')
@crossdomain(origin='*', headers='Content-Type')
def showLinks():
    title = "This is the title";
    return render_template('templates/display.html')



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
