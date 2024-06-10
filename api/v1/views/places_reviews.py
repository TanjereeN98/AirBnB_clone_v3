#!/usr/bin/python3
"""Review route"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """get a list of reviews """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    places = [obj.to_dict() for obj in place.reviews]
    return make_response(jsonify(places), 200)


@app_views.route('reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """get review by id"""
    review = storage.get(Review, review_id)
    return make_response(jsonify(review.to_dict()),
                         200) if review else abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """delete review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """create a new review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review = request.get_json()
    if not review:
        return make_response("Not a JSON", 400)
    if not review.get('user_id'):
        return make_response("Missing user_id", 400)
    user = storage.get(User, review.get('user_id'))
    if not user:
        abort(404)
    if not review.get('text'):
        return make_response("Missing text", 400)

    review["place_id"] = place_id
    new_review = Review(**review)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """update review by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    req_review = request.get_json()
    if not req_review:
        return make_response("Not a JSON", 400)
    ignore = {'id', 'user_id', 'place_id', 'created_at', 'updated_at'}
    for k, v in req_review.items():
        if k not in ignore:
            setattr(review, k, v)
    storage.save()
    return make_response(review.to_dict(), 200)
