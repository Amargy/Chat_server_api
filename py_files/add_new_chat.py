#!/usr/bin/env python3
import flask
from flask import jsonify
from jsonschema import validate, ValidationError
from sqlalchemy import func
from data_base_settings import app, Chat, find_chat_by_name, find_users_by_id, db, User
from validation_schemas import validate_schema_for_new_chat_request


def add_new_chat_in_database(incoming_json):
    max_id_from_database = db.session.query(func.max(Chat.id)).first()[0]
    if max_id_from_database is None:
        max_id_from_database = 0
    new_id = max_id_from_database + 1
    new_chat = Chat(id=new_id, name=incoming_json['name'])
    for user in incoming_json['users']:
        user_integer = int(user)
        user_object_from_database = db.session.query(User).filter(User.id == user_integer).first()
        new_chat.users.append(user_object_from_database)
    db.session.add(new_chat)
    db.session.commit()
    return new_id


@app.route('/chats/add', methods=['POST'])
def post_query_create_chat_between_users():
    incoming_json = flask.request.get_json()
    if incoming_json is None:
        return jsonify("Incoming data is empty"), 204
    try:
        validate(instance=incoming_json, schema=validate_schema_for_new_chat_request)
    except ValidationError:
        return jsonify("Incoming data is not valid"), 204

    if find_chat_by_name(incoming_json['name']) is True:
        return jsonify("Chat with the same name already exists"), 204

    if find_users_by_id(incoming_json['users']) is False:
        return jsonify("User with this name does not exist"), 204

    return jsonify(add_new_chat_in_database(incoming_json)), 200
