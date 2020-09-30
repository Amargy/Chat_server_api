#!/usr/bin/env python3
import flask
from flask import jsonify
from jsonschema import validate, ValidationError
from sqlalchemy import func
from app.data_base_settings import db, User, Message, find_users_in_database, app
from app.validation_schemas import validate_schema_for_new_message


def add_new_message_in_database(incoming_json):
    max_id_from_database = db.session.query(func.max(User.id)).first()[0]
    chat_id_int = int(incoming_json['chat'])
    author_id_int = int(incoming_json['author'])
    new_message = Message(id=max_id_from_database + 1, chat=chat_id_int, author=author_id_int,
                          text=incoming_json['text'])
    db.session.add(new_message)
    db.session.commit()


@app.route('/messages/add', methods=['POST'])
def post_query_send_message():
    incoming_json = flask.request.get_json()
    if incoming_json is None:
        return jsonify(success=False)
        # return response(400, {})
    try:
        validate(instance=incoming_json, schema=validate_schema_for_new_message)
    except ValidationError:
        return jsonify(success=False)
        # return response (405, {})
    else:
        if find_users_in_database(incoming_json['author']) is True:
            add_new_message_in_database(incoming_json)
        else:
            return False
        return jsonify(success=True)
