#!/usr/bin/env python3
import flask
from flask import jsonify, Response
from jsonschema import validate, ValidationError
from sqlalchemy import func
from data_base_settings import User, db, app, find_user_by_username
from validation_schemas import validate_schema_for_new_user_request


def add_new_user_in_database(incoming_json):
    max_id_from_database = db.session.query(func.max(User.id)).first()[0]
    if not max_id_from_database:
        max_id_from_database = 0
    new_id = max_id_from_database + 1
    new_db_object = User(id=new_id, username=incoming_json['username'])
    db.session.add(new_db_object)
    db.session.commit()
    return {'User ID': new_id}


@app.route('/users/add', methods=['POST'])
def post_query_add_new_user():
    incoming_json = flask.request.get_json()
    if not incoming_json:
        return jsonify({'error': 'Incoming data is empty'}), 422
    try:
        validate(instance=incoming_json, schema=validate_schema_for_new_user_request)
    except ValidationError:
        return jsonify({'error': 'Incoming data is not valid'}), 400

    if find_user_by_username(incoming_json['username']):
        return jsonify({'error': 'User with the same name already exists'}), 409

    return jsonify(add_new_user_in_database(incoming_json)), 201
