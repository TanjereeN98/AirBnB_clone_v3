#!/usr/bin/python3
"""view for City objects that handles
all default RESTFul API actions"""

from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route(
    '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """Retrieves the list of all City objects"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in storage.all(City).values()]
    return make_response(jsonify(cities), 200)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """Retrieves a City object by ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return make_response(jsonify(city.to_dict()), 200)


@app_views.route(
    '/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city_by_id(city_id):
    """Deletes a City object by ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route(
    '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city = request.get_json()
    if not request.is_json:
        return make_response("Not a JSON", 400)
    elif 'name' not in city:
        return make_response("Missing name", 400)
    city['state_id'] = state_id
    new_city = City(**city)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """update a city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    req_city = request.get_json()
    if not req_city:
        return make_response("Not a JSON", 400)
    setattr(city, 'name', req_city.get('name'))
    storage.save()
    return make_response(city.to_dict(), 200)
