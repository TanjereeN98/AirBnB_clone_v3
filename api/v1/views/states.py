#!/usr/bin/python3
"""view for State objects that handles
all default RESTFul API actions"""

from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get a list of states"""
    states = [obj.to_dict() for obj in storage.all(State).values()]
    return make_response(jsonify(states), 200)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """Retrieves a State object by ID"""
    state = storage.get(State, state_id)
    if state:
        return make_response(jsonify(state.to_dict()), 200)
    else:
        abort(404)


@app_views.route(
    '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state_by_id(state_id):
    """Deletes a State object by ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response({}, 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a state"""
    state = request.get_json()
    if not request.is_json:
        return make_response("Not a JSON", 400)
    elif 'name' not in state:
        return make_response("Missing name", 400)
    new_state = State(**state)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a state"""
    current_state = storage.get(State, state_id)
    if not current_state:
        abort(404)
    updated_state = request.get_json()
    if not request.is_json:
        return make_response("Not a JSON", 400)
    setattr(current_state, 'name', updated_state.get('name'))
    storage.save()
    return make_response(current_state.to_dict(), 200)
