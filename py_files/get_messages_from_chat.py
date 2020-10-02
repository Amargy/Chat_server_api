#!/usr/bin/env python3
import flask
from flask import jsonify
from jsonschema import validate, ValidationError
from data_base_settings import db, Message, app, find_chat_by_id
from validation_schemas import validate_schema_for_get_message_list


def form_message_dict(message):
    result_dict = {'id': message.id,
                   'chat': message.chat,
                   'author': message.author,
                   'text': message.text,
                   'created_at': message.created_at.strftime("%m/%d/%Y, %H:%M:%S")}
    return result_dict


def form_message_list_from_data_base(incoming_json):
    result = db.session.query(Message).filter(Message.chat == incoming_json['chat']).order_by(Message.created_at).all()
    list_dicts_messages = []
    for message in result:
        list_dicts_messages.append(form_message_dict(message))
    return list_dicts_messages


@app.route('/messages/get', methods=['POST'])
def get_messages_from_chat():
    incoming_json = flask.request.get_json()
    if incoming_json is None:
        return jsonify("Incoming data is empty")
    try:
        validate(instance=incoming_json, schema=validate_schema_for_get_message_list)
    except ValidationError:
        return jsonify("Incoming data is not valid")

    if find_chat_by_id(incoming_json['chat']) is False:
        return jsonify("Chat with this name does not exist")

    message_list = form_message_list_from_data_base(incoming_json)
    return jsonify(message_list)
