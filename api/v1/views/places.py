#!/usr/bin/python3
"""Place route"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """get a list of places"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [obj.to_dict() for obj in city.places]
    return make_response(jsonify(places), 200)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    """get place by id"""
    place = storage.get(Place, place_id)
    return make_response(jsonify(place.to_dict()),
                         200) if place else abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """create a new place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    place = request.get_json()
    if not place:
        return make_response("Not a JSON", 400)
    if not place.get('user_id'):
        return make_response("Missing user_id", 400)
    user = storage.get(User, place.get('user_id'))
    if not user:
        abort(404)
    if not place.get("name"):
        return make_response("Missing name", 400)
    place['city_id'] = city_id
    new_place = Place(**place)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """update a place by id"""
    cur_place = storage.get(Place, place_id)
    if not cur_place:
        abort(404)
    new_place = request.get_json()
    if not new_place:
        return make_response("Not a JSON", 400)
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in new_place.items():
        if key not in ignored_keys:
            setattr(cur_place, key, value)
    storage.save()
    return make_response(cur_place.to_dict(), 200)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """delete place by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response({}, 200)
