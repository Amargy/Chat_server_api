#!/usr/bin/env python3
import flask
from flask import jsonify
from jsonschema import validate, ValidationError
from sqlalchemy import func
from data_base_settings import User, db, app, find_users_in_database
from validation_schemas import validate_schema_for_new_user_request


def add_new_user_in_database(incoming_json):
    max_id_from_database = db.session.query(func.max(User.id)).first()[0]
    if max_id_from_database is None:
        max_id_from_database = 0
    new_db_object = User(id=max_id_from_database + 1, username=incoming_json['username'])
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
        if find_users_in_database(incoming_json['username']) is False:
            add_new_user_in_database(incoming_json)
        else:
            return jsonify("User with the same name already exists")
        return jsonify(success=True)
