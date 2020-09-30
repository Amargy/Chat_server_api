#!/usr/bin/env python3
import flask
from flask import jsonify
from jsonschema import validate, ValidationError
from data_base_settings import User, db, app
from validation_schemas import validate_schema_for_new_user_request


def add_new_user_in_database(incoming_json):
    new_db_object = User(id=incoming_json['id'], username=incoming_json['username'])
    db.session.add(new_db_object)
    db.session.commit()


@app.route('/users/add', methods=['POST'])
def post_query_add_new_user():
    incoming_json = flask.request.get_json()
    if incoming_json is None:
        return jsonify(success=False)
        # return response(400, {})
    try:
        validate(instance=incoming_json, schema=validate_schema_for_new_user_request)
    except ValidationError:
        return jsonify(success=False)
        # return response (405, {})
    else:
        add_new_user_in_database(incoming_json)
        return jsonify(success=True)
