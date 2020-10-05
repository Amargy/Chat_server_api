#!/usr/bin/env python3
import flask
from flask import jsonify
from jsonschema import validate, ValidationError
from sqlalchemy import func
from data_base_settings import db, Message, app, find_chat_by_id, find_users_by_id
from validation_schemas import validate_schema_for_new_message


def add_new_message_in_database(incoming_json):
    max_id_from_database = db.session.query(func.max(Message.id)).first()[0]
    if not max_id_from_database:
        max_id_from_database = 0
    new_id = max_id_from_database + 1
    chat_id_int = int(incoming_json['chat'])
    author_id_int = int(incoming_json['author'])
    new_message = Message(id=new_id, chat=chat_id_int, author=author_id_int,
                          text=incoming_json['text'])
    db.session.add(new_message)
    db.session.commit()
    return {'Message ID': new_id}


@app.route('/messages/add', methods=['POST'])
def post_query_send_message():
    incoming_json = flask.request.get_json()
    if not incoming_json:
        return jsonify({'error': 'Incoming data is empty'}), 422
    try:
        validate(instance=incoming_json, schema=validate_schema_for_new_message)
    except ValidationError:
        return jsonify({'error': 'Incoming data is not valid'}), 400

    if not find_chat_by_id(incoming_json['chat']):
        return jsonify({'error': 'Chat with this name does not exist'}), 406

    if not find_users_by_id(incoming_json['author']):
        return jsonify({'error': 'User with this name does not exist'}), 406

    return jsonify(add_new_message_in_database(incoming_json)), 201
