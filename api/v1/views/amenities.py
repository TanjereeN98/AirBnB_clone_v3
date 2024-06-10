#!/usr/bin/python3
"""view for Amenity objects that handles
all default RESTFul API actions"""

from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenitites = [amenity.to_dict()
                  for amenity in storage.all(Amenity).values()]
    return make_response(jsonify(amenitites), 200)


@app_views.route(
    '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Retrieves an Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return make_response(jsonify(amenity.to_dict()), 200)


@app_views.route(
    '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """Deletes an Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity(state_id):
    """Creates an Amenity"""
    amenity = request.get_json()
    if not request.is_json:
        return make_response("Not a JSON", 400)
    elif 'name' not in amenity:
        return make_response("Missing name", 400)
    new_amenity = Amenity(**amenity)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """update an amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    new_amenity = request.get_json()
    if not request.is_json:
        return make_response("Not a JSON", 400)
    setattr(amenity, 'name', new_amenity.get('name'))
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
