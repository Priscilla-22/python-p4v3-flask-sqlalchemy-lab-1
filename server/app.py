# server/app.py
# !/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


# Add views here
@app.route('/earthquakes/<int:id>')
def earthquakes_get_by_id(id):
    earthquake = db.session.get(Earthquake, id)
    if earthquake:
        body = {
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        }
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404

    return make_response(body, status)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_filter_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    count = len(earthquakes)
    body = [{
        'id': earthquake.id,
        'location': earthquake.location,
        'magnitude': earthquake.magnitude,
        'year': earthquake.year
    } for earthquake in earthquakes]

    response = {'count': count, 'quakes': body}
    status = 200

    return make_response(response, status)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
