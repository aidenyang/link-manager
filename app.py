#!flask/bin/python
from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:231137@localhost/link'

class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text)
    url = db.Column(db.Text)
    type = db.Column(db.Integer)
    date_added = db.Column(db.DateTime)

@app.route('/links', methods=['GET'])
def links():
    if request.method == 'GET':
        results = Link.query.limit(10).offset(0).all()

        json_results = []
        for result in results:
            d = {
                    'id': result.id,
                    'title': result.title,
                    'url': result.url,
                    'type': result.type,
                    'date_added' : result.date_added
                }
            json_results.append(d)
        return jsonify(items=json_results)

if __name__ == '__main__':
    app.run(debug=True)
