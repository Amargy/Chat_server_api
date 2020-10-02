#!/usr/bin/env python3
import flask
from flask import jsonify
from jsonschema import validate, ValidationError
from sqlalchemy import func
from data_base_settings import *
from validation_schemas import validate_schema_for_new_chat_request


def add_new_chat_in_database(incoming_json):
    max_id_from_database = db.session.query(func.max(Chat.id)).first()[0]
    if max_id_from_database is None:
        max_id_from_database = 0
    new_chat = Chat(id=max_id_from_database + 1, name=incoming_json['name'])
    for user in incoming_json['users']:
        user_integer = int(user)
        user_object_from_database = db.session.query(User).filter(User.id == user_integer).first()
        new_chat.users.append(user_object_from_database)
    db.session.add(new_chat)
    db.session.commit()


@app.route('/chats/add', methods=['POST'])
def post_query_create_chat_between_users():
    incoming_json = flask.request.get_json()
    if incoming_json is None:
        return jsonify(success=False)
        # return response(400, {})
    try:
        validate(instance=incoming_json, schema=validate_schema_for_new_chat_request)
    except ValidationError:
        return jsonify(success=False)
        # return response (405, {})
    else:
        if find_users_in_database(incoming_json['users']) is True:
            add_new_chat_in_database(incoming_json)
        else:
            return False
        return jsonify(success=True)
