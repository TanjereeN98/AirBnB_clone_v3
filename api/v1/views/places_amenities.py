#!/usr/bin/python3
""" View for Place's Amenity objects that handles all RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from models.user import User
import models


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities_of_place(place_id):
    """get amenities of place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = [obj.to_dict() for obj in place.amenities]
    return make_response(jsonify(amenities), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """delete place's amenitie by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if models.storage_t == "db":
        amenities_of_place = place.amenities
    else:
        amenity = amenity_id
        amenities_of_place = place.amenity_ids

    if amenity not in amenities_of_place:
        abort(404)

    amenities_of_place.remove(amenity)
    storage.save()
    return make_response({}, 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def add_amenity_to_place(place_id, amenity_id):
    """add_amenity_to_place"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if models.storage_t == "db":
        amenities_of_place = place.amenities
    else:
        amenity = amenity_id
        amenities_of_place = place.amenity_ids

    code = 200
    if amenity not in amenities_of_place:
        amenities_of_place.append(amenity)
        storage.save()
        code = 201

    return make_response(jsonify(
        amenity.to_dict() if models.storage_t == "db" else amenity_id), code)
