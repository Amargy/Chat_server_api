#!/usr/bin/env python3
import flask
from flask import jsonify
from jsonschema import validate, ValidationError
from sqlalchemy import func
from data_base_settings import db, Message, app, find_chat_by_id, find_users_by_id
from validation_schemas import validate_schema_for_new_message


def add_new_message_in_database(incoming_json):
    max_id_from_database = db.session.query(func.max(Message.id)).first()[0]
    if max_id_from_database is None:
        max_id_from_database = 0
    new_id = max_id_from_database + 1
    chat_id_int = int(incoming_json['chat'])
    author_id_int = int(incoming_json['author'])
    new_message = Message(id=new_id, chat=chat_id_int, author=author_id_int,
                          text=incoming_json['text'])
    db.session.add(new_message)
    db.session.commit()
    return new_id


@app.route('/messages/add', methods=['POST'])
def post_query_send_message():
    incoming_json = flask.request.get_json()
    if incoming_json is None:
        return jsonify("Incoming data is empty"), 204
    try:
        validate(instance=incoming_json, schema=validate_schema_for_new_message)
    except ValidationError:
        return jsonify("Incoming data is not valid"), 204

    if find_chat_by_id(incoming_json['chat']) is False:
        return jsonify("Chat with this name does not exist"), 204

    if find_users_by_id(incoming_json['author']) is False:
        return jsonify("User with this name does not exist"), 204

    return jsonify(add_new_message_in_database(incoming_json)), 200
